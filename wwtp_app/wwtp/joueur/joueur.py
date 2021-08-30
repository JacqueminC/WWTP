from flask import Blueprint, render_template,session, request, redirect, url_for, flash, jsonify
from werkzeug.utils import redirect
from table.model import Table
from evaluation.model import Evaluation
from .model import Joueur, AccountForm, AdminTable, RegisterForm
from bson import ObjectId
from wtforms.validators import InputRequired, ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

bpJoueur = Blueprint("joueur", __name__, template_folder="templates", static_folder='static', static_url_path='assets')

@bpJoueur.route("/joinTable", methods=["GET", "POST"])
def joinTable():

    if request.method == "POST":

        if request.form.get("join"): 
            user = session["user"]
            jPseudo = user["pseudo"]
            jId = user["idJoueur"] 
            jNote = user["note"]

            table = Table.findTable(request.values["join"])
            joueur = Joueur.findPlayerById(jId)

            result = Table.canJoinTable(table, joueur, jNote)

            if result:
                hote = table["hote"]
                
                joueurHote = Joueur.findPlayerById(hote["idJoueur"])
                Joueur.joinTable(jId, table["_id"])

                subject = "Un joueur a rejoint votre table"
                body = f"{jPseudo} a rejoint votre table du {table['date']}\n\nWWTP"
                Joueur.sendEmail([joueurHote['email']], subject, body)

                flash('Vous avez rejoint la table de ' + hote["pseudo"] + ' à ' + table["ville"] + ' le ' + str(table['date']), 'info')
                return redirect(url_for('table.listeTable'))    

            else:
                flash('Impossible de rejoindre la table vous ne remplisez pas les conditions !!!', 'error')
                return redirect(url_for('table.listeTable'))

    else:
        flash('Une erreur c\'est produite veuillez réessayer !', 'error')
        return redirect(url_for('table.listeTable'))

@bpJoueur.route("/leaveTable", methods=["GET", "POST"])
def leaveTable():

    if request.method == "POST":

        if request.form.get("leave"):
            user = session["user"]
            idJoueur = user["idJoueur"]
            idTable = request.values["leave"]         
            Joueur.leaveTable(idJoueur, idTable)

            table = Table.findTable(idTable)
            hote = table["hote"]
            Evaluation.createEvaluation(idTable, idJoueur, hote["idJoueur"], 0, "leave")

            note = Evaluation.calculateNote(idJoueur)

            user = session.get('user')
            user["note"] = round(note, 2)
            session.update(user)

            flash("Vous avez quitter la table, vous avez subit un malus sur votre note !", "error")        
            return redirect(url_for('table.tableJoueur'))

        else:
            return redirect(url_for('table.tableJoueur'))

    else:
        return redirect(url_for('table.tableJoueur'))

@bpJoueur.route("/manageTable", methods=["GET", "POST"])
def manageTable():

    if request.method == "POST":
        user = session["user"]
        idJoueur = user["idJoueur"]
        joueur = Joueur.findPlayerById(idJoueur)
        emails = []
        subject = ""
        body = ""        

        if request.form.get("validate"):
            table = Table.findTable(request.values["validate"])
            hote = table["hote"]

            if len(table["joueurs"]) != 0:
                Joueur.validateTable(request.values["validate"])
                subject = "Une table a été validé"
                body = f"La table de {hote['pseudo']} du {table['date']} a été validée ! \n\nVous trouverez ci dessous les informations pour participer à la table :\n\t{joueur['rue']} {joueur['numero']},\n\t{joueur['codePostal']} {joueur['ville']}\n\t{joueur['nom']} {joueur['prenom']}\n\t{joueur['email']}\n\nBon amusement !" 
                flash("La table a été validée, les joueurs receveront l'information par email.", "done")
            else:
                flash("Vous ne pouvez pas valider une table pour laquelle il n'y a aucun joueur.", "error")

        elif request.form.get("close"): 
            idTable = request.values["close"]
            table = Table.findTable(idTable)
            hote = table["hote"]

            Table.closeTable(request.values["close"])

            for joueur in table["joueurs"]:
                Evaluation.createEvaluation(idTable, idJoueur, joueur["idJoueur"], 0, "close")

            note = Evaluation.calculateNote(idJoueur)

            user = session.get('user')
            user["note"] = round(note, 2)
            session.update(user)

            Joueur.sendMailCloseByPlayer(hote, table)

            flash("Votre table a bien été annulé, vous avez subit un malus sur votre note !", "error")
        
    return redirect(url_for('table.tableHote'))

@bpJoueur.route("/evaluer", methods=["GET", "POST"])
def evaluatePlayer():

    if session.get("isLogged"):

        user = session["user"]
        idJoueur = user["idJoueur"]
        dictTable = {}       

        tables = Table.findTableForNoteByIdJoueurAndPast(idJoueur)

        for table in tables:
            dictJoueur = {}    
            dictData = {}  

            joueurs = table["joueurs"]
            hote = table["hote"]
            idTable = table["_id"]

            if hote["idJoueur"] != ObjectId(idJoueur):
                eval = Evaluation.findNoteByEvaluateurAndEvalue(idJoueur, hote["idJoueur"], idTable)
                dictJoueur[str(hote["pseudo"])] = [ eval, str(hote["idJoueur"])]
            
            for j in joueurs:
                if j["idJoueur"] != ObjectId(idJoueur):
                    eval = Evaluation.findNoteByEvaluateurAndEvalue(idJoueur, j["idJoueur"], idTable)
                    dictJoueur[str(j["pseudo"])] = [ eval, str(j["idJoueur"])]

            if len(dictJoueur) >= 1:

                infoTable = [ str(table["date"]), table["hote"]["pseudo"], table["ville"], str(table["hote"]["idJoueur"]) ]

                dictData["joueurs"] = dictJoueur
                dictData["infoTable"] = infoTable

                dictTable[str(idTable)] = dictData

        return render_template("evaluer.html", dictTable=dictTable)
    else:
        return redirect("/")

@bpJoueur.route("/inscription", methods=["GET", "POST"])
def formInscription():
    form = RegisterForm()

    if session.get("isLogged") != True:

        if form.validate_on_submit():
            try:
                Joueur.createPlayer(form)
                flash("Inscription réussie", 'registerDone')
                return redirect(url_for("auth.login"))
                
            except Exception as ex:
                flash(ex, "error")
                return render_template("formInscription.html", form=form, ve=ValidationError())

        return render_template("formInscription.html", form=form)
    else:
        return redirect("/")

@bpJoueur.route("/account", methods=["GET", "POST"])
def account():

    if session.get("isLogged") == True:
        form = AccountForm()

        joueur = Joueur.findPlayerById(session["user"]["idJoueur"])

        form.nom.data = joueur["nom"]
        form.prenom.data = joueur["prenom"]
        form.rue.data = joueur["rue"]
        form.numero.data = joueur["numero"]
        form.boite.data = joueur["boite"]
        form.codePostal.data = joueur["codePostal"]
        form.ville.data = joueur["ville"]
        form.email.data = joueur["email"]
        form.pseudo.data = joueur["pseudo"]
        form.dateDeNaissance.data = joueur["dateDeNaissance"]

        if form.validate_on_submit():
            try:
                Joueur.updatePlayer(form, joueur)
                flash("Votre compte à été mis à jour", "done")
                return redirect(url_for("joueur.account"))
            except Exception as ex:
                flash(ex, "error")
                return render_template("account.html", form=form, ve=ValidationError())

        return render_template("account.html", form=form)
    else:
        return redirect("/")

@bpJoueur.route("/adminJ", methods=["GET", "POST"])
def adminjoueur():

    if session.get("isLogged") == True and session.get("isAdmin") == True:

        joueurs = Joueur.getAllPlayers()

        if request.form.get("lock"):
            Joueur.lockPlayer(request.values["lock"])

        return render_template("adminJoueur.html", joueurs=joueurs)

    else:
        return redirect("/")
    

@bpJoueur.route("/lock", methods=["GET", "POST"])
def lock():

    if session.get("isLogged") == True and session.get("isAdmin") == True:

        if request.form.get("lock"):
            Joueur.lockPlayer(request.values["lock"])

        return redirect(url_for('joueur.adminjoueur'))

    else:
        return redirect("/")

@bpJoueur.route("/adminT", methods=["GET", "POST"])
def adminTable():   

    if session.get("isLogged") == True and session.get("isAdmin") == True:

        now = datetime.today()
        tables = Table.getAllTables()
        form = AdminTable()

        if form.validate_on_submit():
            s = form.temps.data
            if s != "all":
                if s == "past":
                    tables = Table.findTableByDatePast()
                elif s == "futur":
                    tables = Table.findTableByDateFutur()
                elif s == "all":
                    tables = Table.getAllTables()
            
        else:
            tables = Table.getAllTables()
        

        return render_template("adminTable.html", tables=tables, form=form, now=now)

    else:
        return redirect("/")

@bpJoueur.route("/close", methods=["GET", "POST"])
def close():

    if session.get("isLogged") == True and session.get("isAdmin") == True:

        if request.form.get("close"):
            Table.closeTable(request.values["close"])

            Joueur.sendMailCloseByAdmin(request.values["close"])

        return redirect(url_for('joueur.adminTable'))

    else:
        return redirect("/")

    


