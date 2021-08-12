import re
from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, PasswordField
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
            flash("L'email est déjà utilisé", "email")
            return ValidationError()


    def validate_pseudo(self, pseudo):
        p, find = Joueur.findPseudoExist(pseudo.data)

        if not find:
            flash("Le pseudo n'est pas disponible, essayé " + p, "pseudo")
            return ValidationError()

    


@bpJoueur.route("/joinTable", methods=["GET", "POST"])
def joinTable():

    if request.method == "POST":

        if request.form.get("join"): 
            user = session["user"]
            jPseudo = user["pseudo"]
            jId = user["idJoueur"] 

            table = Table.findTable(request.values["join"])
            joueur = Joueur.findPlayerById(jId)
            result = Table.canJoinTable(table, joueur)

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
                body = f"La table de {hote['pseudo']} du {table['date']} a été validée ! \n\nVous trouverez ci dessous les informations pour participer à la table :\n\t{joueur['rue']} {joueur['numero']},\n\t{joueur['codePostal']}{joueur['ville']}\n\t{joueur['nom']} {joueur['prenom']}\n\t{joueur['email']}\n\nBon amusement !" 
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
            body = f"La table de {hote['pseudo']} du {table['date']} a été annulée !\n\nWWTP"
            flash("Votre table a bien été annulé, vous avez subit un malus sur votre note !", "done")

        for joueur in table["joueurs"]:
            emails = emails + [joueur["email"]]

        if len(emails) > 0:
            Joueur.sendEmail(emails, subject, body)
        
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
                flash("Inscription Réussi", 'registerDone')
                return render_template("formInscription.html", form=registerForm())
                
            except Exception as ex:
                flash(ex, 'error')
                return render_template("formInscription.html", form=form, ve=ValidationError())
            


        return render_template("formInscription.html", form=form)
    else:
        return redirect("/")


