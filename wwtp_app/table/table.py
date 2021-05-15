from flask import Blueprint, app, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FormField, FieldList
from wtforms.fields.html5 import IntegerRangeField, DateTimeField, DateField, TimeField
from wtforms.form import Form

bpTable = Blueprint("table", __name__, template_folder="templates")

class JeuxListeForm(Form):
    nom = StringField("Nom ")
    version = StringField("Version ")

class CreationTableForm(FlaskForm):
    jeuxLibre = BooleanField(' Jeux libre ?')
    nbPlace = IntegerField('Nombre de place disponnible')
    jeux = FieldList(FormField(JeuxListeForm), min_entries=3)
    date = DateField('Date', format='%Y-%m-%d')
    heure = TimeField('Heure')
    ville = StringField('Ville')
    ageMin = BooleanField('Définir un âge minimum ?')
    age = IntegerField(' Age minimum ?')
    regle = BooleanField(' Connaissance des règles requises ?')
    noteMin = BooleanField(' Note minimum ?')
    note = IntegerRangeField('Note')

@bpTable.route("/tableForm", methods=["GET", "POST"])
def creationTable():
    form = CreationTableForm()

    if form.validate_on_submit():
        return "Form envoyé! {} and {}".format(form.jeuxLibre.data, form.date.data)

    return render_template("tableForm.html", form=form)
