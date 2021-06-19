from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from pymongo import message
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, BooleanField, FormField, FieldList
from wtforms.fields.html5 import IntegerRangeField, DateField, TimeField
from wtforms.form import Form
from wtforms.validators import InputRequired, ValidationError
from datetime import datetime, timedelta
from wwtp.table.model import Table
from .model import Joueur

bpJoueur = Blueprint("joueur", __name__, template_folder="templates")

@bpJoueur.route("/joinTable", methods=["GET", "POST"])
def joinTable():

    if request.method == "POST":

        if request.form.get("join"):            
            table = Table.findTable(request.values["join"])
            result = Table.canJoinTable(table, session["user"])

            if result:
                user = session["user"]
                idJoueur = user["idJoueur"]
                hote = table["hote"]
                Joueur.joinTable(idJoueur, table["_id"])

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
            Joueur.leaveTable(idJoueur, request.values["leave"])

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
            table = Table.findTable(request.values["close"])
            hote = table["hote"]

            Joueur.closeTable(request.values["close"], idJoueur, len(table["joueurs"]))

            subject = "Une table a été annulée"
            body = f"La table de {hote['nom']} du {table['date']} a été annulée !\n\nWWTP"
            flash("Votre table a bien été annulé, vous avez subit un malus sur votre note !", "done")

        for joueur in table["joueurs"]:
            emails = emails + [joueur["email"]]

        if len(emails) > 0:
            Joueur.sendEmail(emails, subject, body)
        
    return redirect(url_for('table.tableHote'))
