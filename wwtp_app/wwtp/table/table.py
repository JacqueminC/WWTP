from flask import Blueprint, render_template,session, request
from flask_wtf import FlaskForm
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

    def validate_jeux(self, jeux):        
        if self.jeuxLibre.data == False:
            if self.jeux[0].nom.data == None or self.jeux[0].nom.data == "":
                raise ValidationError("Vous devez indiquer un jeu si vous n'êtes pas en jeux libre!")
     

    def validate_age(self, age):
        if self.ageMin.data == True:
            if not isinstance(self.age.data, int):
                raise ValidationError("Veuillez entrez un age en chiffre!")
            if self.age.data == None:
                raise ValidationError("Veuillez indiquer une valeur! L'age doit être entre 16 et 99!")
            if self.age.data < 16 or self.age.data >99:
                raise ValidationError("L'age doit être entre 16 et 99!")
    
    def validate_date(self, date):
        now = datetime.now() + timedelta(hours=2)
        dtString = str(date.data) + " " + str(self.heure.data)
        dtForm = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S')

        print("dtForm : " + str(dtForm))

        if now > dtForm:
            raise ValidationError("La date doit être supérieur à maintenant PLUS 2 heures!")
            

@bpTable.route("/formCreation", methods=["GET", "POST"])
def formCreation():
    form = CreationTableForm()
    done = "ko"

    if form.validate_on_submit():
       #return "Form envoyé! {} and {}".format(form.nbPlace.data, form.ville.data)

       result = Table.canCreateTable(session["idUser"], form.date.data, form.heure.data)

       if result >= 1:
           ve = ValidationError("Impossible de créer une table car vous participez déjà à une table pour le moment choisi")
           return render_template("formCreation.html", form=form, ve=ve, done=done)
       else:
           Table.createTable(form)
           done = "ok"
           return render_template("formCreation.html",form=form, done=done) 
       

    return render_template("formCreation.html", form=form, done=done)

@bpTable.route("/listeTable", methods=["GET", "POST"])
def listeTable():
    tables = Table.findAvalaibleTable(session["idUser"])

    return render_template("listeTable.html", tables=tables)

@bpTable.route("/joinTable", methods=["GET", "POST"])
def joinTable():
    if request.method == "POST":
        if request.form.get("join"):
            print(session["user"])
            print(request.values["join"])
            result = Table.canJoinTable(request.values["join"], session["user"])
            if result:
                print("ok")
            else:
                print("not ok")
            return request.values["join"]
