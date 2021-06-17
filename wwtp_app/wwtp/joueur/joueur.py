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

            flash("Vous avez quitter la table, vous avez subit un malus sur votre note")        
            return redirect(url_for('table.tableJoueur'))

        else:
            return redirect(url_for('table.tableJoueur'))

    else:
        return redirect(url_for('table.tableJoueur'))
