from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, PasswordField, RadioField
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import EmailField, DateField
from table.model import Table
from evaluation.model import Evaluation
from .model import Joueur
from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

bpJoueur = Blueprint("joueur", __name__, template_folder="templates")

class accountForm(FlaskForm):
    nom = StringField("Nom", validators=[InputRequired()])
    prenom = StringField("Prénom", validators=[InputRequired()])
    rue = StringField("Rue", validators=[InputRequired()])
    numero = IntegerField("Numéro", validators=[InputRequired()])
    boite = StringField("Boite")
    codePostal = StringField("Code postal", validators=[InputRequired()])
    ville = StringField("Ville", validators=[InputRequired()])
    dateDeNaissance = DateField('Date de naissance', format='%Y-%m-%d', render_kw={'disabled':''})
    pseudo = StringField("Pseudo", render_kw={'disabled':''})
    email = EmailField("Email", render_kw={'disabled':''})
    motDePasse = PasswordField("Mot de passe")
    confMDP = PasswordField("Confirmation du mot de passe")

    def validate_confMDP(self, confMDP):
        if self.motDePasse.data != None and self.motDePasse.data != "":
            if confMDP.data != self.motDePasse.data:
                flash("La validation n'est pas correcte", "confmdp")
                return ValidationError()    

class registerForm(FlaskForm):
    nom = StringField("Nom", validators=[InputRequired()])
    prenom = StringField("Prénom", validators=[InputRequired()])
    rue = StringField("Rue", validators=[InputRequired()])
    numero = IntegerField("Numéro", validators=[InputRequired()])
    boite = StringField("Boite")
    codePostal = StringField("Code postal", validators=[InputRequired()])
    ville = StringField("Ville", validators=[InputRequired()])
    dateDeNaissance = DateField('Date de naissance', format='%Y-%m-%d', validators=[InputRequired()])
    pseudo = StringField("Pseudo", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    motDePasse = PasswordField("Mot de passe", validators=[InputRequired()])
    confMDP = PasswordField("Confirmation du mot de passe", validators=[InputRequired()])

class AdminTable(FlaskForm):
    temps = RadioField('Label', choices=[('all','Tout'),('past','Passé'),('futur','Futur')], default='all')
    

    def validate_dateDeNaissance(self, dateDeNaissance):
        now = datetime.today()
        ageCalcule = relativedelta(now, dateDeNaissance.data).years

        if ageCalcule < 15:
            flash("Il faut avoir 15 ans pour s'inscrire sur le site", ("ddn"))
            return ValidationError()

    def validate_confMDP(self, confMDP):
        if confMDP.data != self.motDePasse.data:
            flash("La validation n'est pas correcte", "confmdp")
            return ValidationError()

    def validate_email(self, email):
        result = Joueur.findEmailExist(email.data)

        if result != 0:
            email.data = ""
            flash("L'email est déjà utilisé", "email")
            return ValidationError()

    def validate_pseudo(self, pseudo):
        p, find = Joueur.findPseudoExist(pseudo.data)

        if not find:
            pseudo.data = p
            flash("Le pseudo n'est pas disponible, essayé " + p, "pseudo")
            return ValidationError()


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

                subject = "Un joueur à rejoints votre table"
                body = f"{jPseudo} a rejoint votre table du {table['date']}\n\nWWTP"
                Joueur.sendEmail([joueurHote['email']], subject, body)

                flash('Vous avez rejoins la table de ' + hote["pseudo"] + ' à ' + table["ville"] + ' le ' + str(table['date']), 'info')
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

            flash("Vous avez quitter la table, vous avez subit un malus sur votre note !")        
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

    flash("Votre table a bien été annulé, vous avez subit un malus sur votre note !", "done")
        
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
    form = registerForm()

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
        form = accountForm()

        joueur = Joueur.findPlayerById(session["user"]["idJoueur"])

        if not form.is_submitted():       

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
            Joueur.updatePlayer(form, joueur)
            return redirect(url_for("joueur.account"))


        return render_template("account.html", form=form)
    else:
        return redirect("/")

@bpJoueur.route("/adminJ", methods=["GET", "POST"])
def adminjoueur():

    if session.get("isLogged") == True and session.get("isAdmin") == True:

        joueurs = Joueur.getAllPlayers()

        if request.form.get("lock"):
            print(request.values["lock"])
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

    


