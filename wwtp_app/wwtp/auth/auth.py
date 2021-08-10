from flask import Blueprint, render_template, request, flash, session, redirect
from flask_wtf.form import FlaskForm
from wtforms.fields.core import StringField
from wtforms import PasswordField
from wtforms.validators import InputRequired, ValidationError
from joueur.model import Joueur
from evaluation.model import Evaluation

bpAuth = Blueprint("auth", __name__, template_folder="templates")

class authFrom(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    mdp = PasswordField("Mot de passe", validators=[InputRequired()])

@bpAuth.route("/", methods=["GET", "POST"])
def login():
    form = authFrom()

    if form.validate_on_submit():
        data = request.form.to_dict()
        user = Joueur.findPlayerByEmailAndAccess(data.get("email"))

        connect = False

        if user == None:
            connect = False
        else :
            if "motDePasse" in user:
                if Joueur.verifyPassword(user["motDePasse"], data.get("mdp")):
                    connect = True
                else:
                    connect = False

        if connect:
            """
            {'_id': ObjectId('6106ab185bf4e8dec342ad2e'), 
            'pseudo': 'Test1234', 
            'email': 'cedjacq@outlook.com', 
            'motDePasse': secret',
            'nom': 'Jacquemin', 'prenom': 'Cédric', 'rue': 'rue des Sport', 'numero': 2, 'boite': '', 'ville': 'Strepy-Bracquegnies', 'codePostal': '7110', 'dateDeNaissance': '1988-10-08', 'dateDeCreation': datetime.datetime(2021, 8, 1, 16, 9, 28, 90000), 'estBloque': False}"""

            note = Evaluation.calculateNote(user["_id"])

            session["isLogged"] = connect
            session["user"] = {
                "pseudo": user["pseudo"],
                "firstName": user["prenom"],
                "note": note,
                "idJoueur": str(user["_id"])
            }
            return redirect("/home")
        else:
            flash("Email et / ou mot de passe incorrect !", "errLog")
            return render_template("auth.html", form=form)

    return render_template("auth.html", form=form)

@bpAuth.route("/logout", methods=["GET", "POST"])
def logout():
    
    session.pop("user", None)
    session["isLogged"] = False

    return redirect("/")