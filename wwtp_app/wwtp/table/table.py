from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, ValidationError
from datetime import datetime, timedelta
from .model import Table, CreationTableForm
from joueur.model import Joueur

bpTable = Blueprint("table", __name__, template_folder="templates", static_folder='static', static_url_path='assets')


@bpTable.route("/formCreation", methods=["GET", "POST"])
def formCreation():
    if session.get("isLogged"):
        form = CreationTableForm()
        form.ville.data = session["user"]["ville"]
        done = "ko"

        if form.validate_on_submit():

            user = session["user"]
            idJoueur = user["idJoueur"]

            result = Table.canCreateTable(idJoueur, form.date.data, form.heure.data)

            if result >= 1:
                ve = ValidationError()
                flash("Impossible de créer une table car vous participez déjà à une table pour le moment choisi !!!", 'error')
                return render_template("formCreation.html", form=form, ve=ve, done=done)
            else:
                try:
                    Table.createTable(form)
                    done = "ok"
                    flash('Votre table à bien été créé !', 'info')
                    return redirect(url_for('table.formCreation'))
                except Exception as ex:
                    flash(ex)
                    return render_template("formCreation.html", form=form)
        

        return render_template("formCreation.html", form=form, done=done)
    else:
        return redirect("/")


@bpTable.route("/listeTable", methods=["GET", "POST"])
def listeTable():
    if session.get("isLogged"):
        user = session["user"]
        
        tables = Table.findAvalaibleTable(user["idJoueur"])

        return render_template("listeTable.html", tables=tables)
    else:
        return redirect("/")


@bpTable.route("/tableJoueur", methods=["GET", "POST"])
def tableJoueur():
    if session.get("isLogged"):
        user = session["user"]
        id = user["idJoueur"]
        result = Table.findTableByPlayerAndValidity(id)
        return render_template("tablesJoueur.html", result=result)
    else:
        return redirect("/")

@bpTable.route("/tableHote", methods=["GET", "POST"])
def tableHote():
    if session.get("isLogged"):
        user = session["user"]
        id = user["idJoueur"]
        result = Table.findTableByHostAndValidity(id)
        return render_template("tablesHote.html", result=result)
    else:
        return redirect("/")


        
