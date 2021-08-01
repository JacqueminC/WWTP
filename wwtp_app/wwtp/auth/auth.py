from flask import Blueprint, render_template, request
from flask_login import login_user
from flask_wtf.form import FlaskForm
from wtforms.fields.core import StringField
from wtforms import PasswordField
from wtforms.validators import InputRequired
from wwtp.joueur.model import Joueur

bpAuth = Blueprint("auth", __name__, template_folder="templates")

class authFrom(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    mdp = PasswordField("Mot de passe", validators=[InputRequired()])

@bpAuth.route("/", methods=["GET"])
def logGet():
    form = authFrom()
    return render_template("auth.html", form=form)

@bpAuth.route("/", methods=["POST"])
def logPost():
    data = request.form.to_dict()
    user = Joueur.findPlayerByEmail(data.get("email"))

    print(user)
    print(user["motDePasse"])
    print(data.get("mdp"))

    if user == None:
        return "None"
    else :
        if "motDePasse" in user:
            if Joueur.verifyPassword(user["motDePasse"], data.get("mdp")):
                return "match pwd"


    return "not ok"

@bpAuth.route("/logout", methods=["GET, POST"])
def logout():
    return "LOGOUT"