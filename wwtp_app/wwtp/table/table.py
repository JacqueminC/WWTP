from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from pymongo import message
from werkzeug.utils import redirect
from wtforms import StringField, IntegerField, BooleanField, FormField, FieldList
from wtforms.fields.html5 import IntegerRangeField, DateField, TimeField
from wtforms.form import Form
from wtforms.validators import InputRequired, ValidationError
from datetime import datetime, timedelta
from .model import Table

bpTable = Blueprint("table", __name__, template_folder="templates")

class JeuxListeForm(Form):
    nom = StringField("Nom ")
    version = StringField("Version ")

class CreationTableForm(FlaskForm):
    jeuxLibre = BooleanField(' Jeux libre ?')
    nbPlace = IntegerField('Nombre de place disponnible', validators=[InputRequired()])
    jeux = FieldList(FormField(JeuxListeForm), min_entries=1)
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    heure = TimeField('Heure', validators=[InputRequired()])
    ville = StringField('Ville', validators=[InputRequired()])
    ageMin = BooleanField('Définir un âge minimum ?')
    age = IntegerField(' Age minimum ?', default=0)
    regle = BooleanField(' Connaissance des règles requises ?')
    noteMin = BooleanField(' Note minimum ?')
    note = IntegerRangeField('Note', default=0)

    def validate_nbPlace(self, nbPlace):
        if nbPlace.data < 1:
            flash("Il doit y avoir au moins une place de libre pour créer une table", "place")
            return ValidationError()
        if nbPlace.data > 10:
            flash("Le nombre de place maximum est de 10", "place")
            return ValidationError()

    def validate_jeux(self, jeux):        
        if self.jeuxLibre.data == False:
            if jeux[0].nom.data == None or self.jeux[0].nom.data == "":
                flash("Vous devez indiquer un jeu si vous n'êtes pas en jeux libre!", "jeu")
                raise ValidationError()
     

    def validate_age(self, age):
        if self.ageMin.data == True:
            if not isinstance(self.age.data, int):
                flash("Veuillez entrez un age en chiffre!", 'age')
                raise ValidationError()
            if age.data == None:
                flash("Veuillez indiquer une valeur! L'age doit être entre 16 et 99!", 'age')
                raise ValidationError()
            if age.data < 16 or self.age.data >99:
                flash("L'age doit être entre 16 et 99!", 'age')
                raise ValidationError()
    
    def validate_heure(self, heure):
        now = datetime.now() + timedelta(hours=2)
        dtString = str(self.date.data) + " " + str(heure.data)
        dtForm = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S')

        if now > dtForm:
            flash("La date doit être supérieur à maintenant PLUS 2 heures!", "date")
            raise ValidationError()
            

@bpTable.route("/formCreation", methods=["GET", "POST"])
def formCreation():
    form = CreationTableForm()
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
           Table.createTable(form)
           done = "ok"
           flash('Votre table à bien été créé !', 'info')
           return render_template("formCreation.html",form=form, done=done) 
       

    return render_template("formCreation.html", form=form, done=done)

@bpTable.route("/listeTable", methods=["GET", "POST"])
def listeTable():
    user = session["user"]
    tables = Table.findAvalaibleTable(user["idJoueur"])

    return render_template("listeTable.html", tables=tables)

@bpTable.route("/joinTable", methods=["GET", "POST"])
def joinTable():
    if request.method == "POST":
        if request.form.get("join"):
            table = Table.findTable(request.values["join"])
            result = Table.canJoinTable(table, session["user"])
            
            if result:
                user = session["user"]
                id = user["idJoueur"]
                name = user["nom"]
                hote = table["hote"]

                if "joueurs" in table:   
                    joueurs = table["joueurs"]
                    joueurs.append(
                        {
                            "idJoueur" : id,
                            "nom" : name
                        })
                    table["joueurs"] = joueurs

                else:
                    joueurs = []
                    joueurs.append(
                        {
                            "idJoueur" : id,
                            "nom" : name
                        })

                    table["joueurs"] = joueurs

                Table.saveTable(table)
                flash('Vous avez rejoins la table de ' + str(hote) + ' à ' + str(table["ville"]) + ' le ' + str(table['date']), 'info')
                return redirect(url_for('table.listeTable'))    

            else:
                flash('Impossible de rejoindre la table vous ne remplisez pas les conditions !!!', 'error')
                return redirect(url_for('table.listeTable'))

    else:
        flash('Une erreur c\'est produite veuillez réessayer !', 'error')
        return redirect(url_for('table.listeTable'))

@bpTable.route("/tableJoueur", methods=["GET", "POST"])
def tableJoueur():
    user = session["user"]
    id = user["idJoueur"]
    result = Table.findTableByPlayer(id)
    return render_template("tablesJoueur.html", result=result)

@bpTable.route("/tableHote", methods=["GET", "POST"])
def tableHote():
    user = session["user"]
    id = user["idJoueur"]
    result = Table.findTableByHost(id)
    return render_template("tablesHote.html", result=result)


        
