from flask import Blueprint, app, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FormField, FieldList
from wtforms.fields.html5 import IntegerRangeField, DateTimeField, DateField, TimeField
from wtforms.form import Form
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError

bpTable = Blueprint("table", __name__, template_folder="templates")

class JeuxListeForm(Form):
    nom = StringField("Nom ")
    version = StringField("Version ")

class CreationTableForm(FlaskForm):
    jeuxLibre = BooleanField(' Jeux libre ?')
    nbPlace = IntegerField('Nombre de place disponnible', validators=[InputRequired()])
    jeux = FieldList(FormField(JeuxListeForm), min_entries=1)
    date = DateField('Date', format='%Y-%m-%d')
    heure = TimeField('Heure')
    ville = StringField('Ville', validators=[InputRequired()])
    ageMin = BooleanField('Définir un âge minimum ?')
    age = IntegerField(' Age minimum ?', default=0)
    regle = BooleanField(' Connaissance des règles requises ?')
    noteMin = BooleanField(' Note minimum ?')
    note = IntegerRangeField('Note')

    def validate(self):        
        if not Form.validate(self):
            return False
        
        if self.jeuxLibre.data == False and (self.jeux[0].nom.data == None or self.jeux[0].nom.data == ""):
            print("jeux vide")
            return False
        
        return True 

    def validate_age(self, age):
        if self.ageMin.data == True:
            print("check age value")
            if self.age.data == None:
                raise ValidationError("Veuillez indiquer une valeur! L'age doit être entre 16 et 99")
            if self.age.data < 16 or self.age.data >99:
                raise ValidationError("L'age doit être entre 16 et 99")


    
        
         

       

            

@bpTable.route("/tableForm", methods=["GET", "POST"])
def creationTable():
    form = CreationTableForm()

    if form.validate_on_submit():
        return "Form envoyé! {} and {}".format(form.nbPlace.data, form.ville.data)

    return render_template("tableForm.html", form=form)
