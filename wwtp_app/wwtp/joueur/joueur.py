from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wwtp.table.model import Table
from wwtp.evaluation.model import Evaluation
from .model import Joueur
from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, ValidationError

bpJoueur = Blueprint("joueur", __name__, template_folder="templates")

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


@bpJoueur.route("/joinTable", methods=["GET", "POST"])
def joinTable():

    if request.method == "POST":

        if request.form.get("join"):            
            table = Table.findTable(request.values["join"])
            result = Table.canJoinTable(table, session["user"])

            if result:
                user = session["user"]
                jName = user["nom"]
                jId = user["idJoueur"]                
                hote = table["hote"]
                joueurHote = Joueur.findPlayerById(hote["idJoueur"])
                Joueur.joinTable(jId, table["_id"])

                subject = "Un joueur à rejoints votre table"
                body = f"{jName} a rejoint votre table du {table['date']}\n\nWWTP"
                Joueur.sendEmail([joueurHote['email']], subject, body)

                flash('Vous avez rejoins la table de ' + hote["nom"] + ' à ' + table["ville"] + ' le ' + str(table['date']), 'info')
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
                body = f"La table de {hote['nom']} du {table['date']} a été validée ! \n\nVous trouverez ci dessous les informations pour participer à la table :\n\t{joueur['rue']} {joueur['numero']},\n\t{joueur['codePostal']}{joueur['ville']}\n\t{joueur['nom']} {joueur['prenom']}\n\t{joueur['email']}\n\nBon amusement !" 
                flash("La table a été validée, les joueurs receveront l'information par email.", "done")
            else:
                flash("Vous ne pouvez pas valider une table pour laquelle il n'y a aucun joueur.", "error")

        elif request.form.get("close"): 
            idTable = request.values["close"]
            table = Table.findTable(idTable)
            hote = table["hote"]

            Joueur.closeTable(request.values["close"], idJoueur, len(table["joueurs"]))

            for joueur in table["joueurs"]:
                Evaluation.createEvaluation(idTable, idJoueur, player["idJoueur"], 0, "close")

            note = Evaluation.calculateNote(idJoueur)

            user = session.get('user')
            user["note"] = round(note, 2)
            session.update(user)

            subject = "Une table a été annulée"
            body = f"La table de {hote['nom']} du {table['date']} a été annulée !\n\nWWTP"
            flash("Votre table a bien été annulé, vous avez subit un malus sur votre note !", "done")

        for joueur in table["joueurs"]:
            emails = emails + [joueur["email"]]

        if len(emails) > 0:
            Joueur.sendEmail(emails, subject, body)
        
    return redirect(url_for('table.tableHote'))

@bpJoueur.route("/evaluer", methods=["GET", "POST"])
def evaluatePlayer():

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

@bpJoueur.route("/inscription", methods=["GET", "POSTS"])
def formInscription():
    form = registerForm()

    return render_template("formInscription.html", form=form)


