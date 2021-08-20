from bson.objectid import ObjectId
from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from flask_cors.decorator import cross_origin
from flask_wtf.recaptcha.widgets import JSONEncoder
from werkzeug.utils import header_property
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from .model import GameForm, Ludo
import requests

bpLudo = Blueprint("ludo", __name__, template_folder="templates")


@bpLudo.route("/", methods=["GET", "POST"])
def myLudo():  

    """print(requests.get('https://www.boardgamegeek.com/xmlapi/search?search=Catane').content)"""

    form = GameForm()
    idJ = ObjectId(session["user"]["idJoueur"])    

    games = Ludo.findLudoByPlayer(idJ)
    gamesF = Ludo.findLudoFavoriteByPlayer(idJ)

    if form.validate_on_submit():
        try:
            
            ludo = Ludo(idJ, form.nom.data, form.version.data, form.min.data,form.max.data, form.age.data, form.favori.data)

            ludo.createLudo()

        except Exception as ex:
            flash(ex, "error")
            return render_template("ludo.html", form=form, ve=ValidationError())
        
    return render_template("ludo.html", form = form, games=games, gamesF=gamesF)


@bpLudo.route("/action", methods=["GET", "POST"])
def action():
    if request.form.get("trash"):
        print(request.values["trash"])
        Ludo.deleteLudo(request.values["trash"])
    
    if request.form.get("favorite"):
        Ludo.updateFavorite(request.values["favorite"])        

    return redirect(url_for('ludo.myLudo'))
