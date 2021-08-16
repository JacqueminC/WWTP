from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, InputRequired, ValidationError
from flask_wtf import FlaskForm
from .model import GameForm

bpLudo = Blueprint("ludo", __name__, template_folder="templates")





@bpLudo.route("/", methods=["GET", "POST"])
def myLudo():    
    form = GameForm() 

    if form.validate_on_submit():
        try:
            print('ok')
        except Exception as ex:
            flash(ex, "error")
            return render_template("ludo.html", form=form, ve=ValidationError())
        
    return render_template("ludo.html", form = form)

