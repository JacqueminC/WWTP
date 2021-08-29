from .repo import *
from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, FormField, FieldList
from wtforms.fields.html5 import IntegerRangeField, DateField, TimeField
from wtforms.validators import InputRequired, ValidationError
from datetime import datetime, timedelta
from wtforms.form import Form
from flask import session, flash
from joueur.repo import RepoJoueur

repositoryTable = RepoTable()
repositoryJoueur = RepoJoueur()

class Table:

    def __init__(self, hote , jeuxLibre, nbPlace, jeux, date, ville, ageMin, age, regle, noteMin, note):
        now = datetime.today()

        self.hote = hote

        if isinstance(jeuxLibre, bool):
            self.jeuxLibre = jeuxLibre
        else:
            raise Exception("Le format de jeuxLibre n'est pas un boolean")


        if nbPlace < 1:
            raise Exception("Il doit y avoir au moins une place de libre")        
        else:
            if nbPlace > 10:
                raise Exception("Le nombre maximum de place est de 10")
            else:
                self.nbPlace = nbPlace

        if isinstance(jeuxLibre, bool):
            if jeuxLibre == True:
                self.jeux = list()
            elif jeuxLibre == False and len(jeux) < 1:
                self.jeuxLibre = True
            else:
                self.jeux = jeux
        else:
            raise Exception("Le format de jeuxLibre n'est pas un boolean")
            

        if date < datetime.today() + timedelta(hours=2):
            raise Exception("La date ne peut pas être antérieur à la date actuelle PLUS 2h")
        else:
            if isinstance(date, datetime):
                self.date = date
            else:
                raise Exception("Le format de la date n'est pas une string")          
        
        if ville == "" or ville == None:
            raise Exception("La ville ne peut pas être vide")
        else:
            if isinstance(ville, str):
                self.ville = ville
            else:
                raise Exception("Le format de la ville n'est pas une string")

        if isinstance(ageMin, bool):
            self.ageMin = ageMin
        else:
            raise Exception("Le format de l'ageMin n'est pas un boolean")

        if ageMin == True:
            if isinstance(age, int):
                if age >= 16 and age <= 99:
                    self.age = age
                else:
                    raise Exception("L'âge ne doit être compris entre 16 et 99")
            else:
                raise Exception("Le format de l'age n'est pas un integer")  

        if isinstance(regle, bool):
            self.regle = regle
        else:
            raise Exception("Le format de regle n'est pas un boolean")

        self.noteMin = noteMin

        if noteMin == True:
            if isinstance(note, int):
                if note >= 0 and note <= 5:
                    self.note = note
                else:
                    raise Exception("La note ne peut pas être suppérieur à 5 et inférieur à 0")
            else:
                raise Exception("La note doit être un integer")

        self.joueurs = []
        self.estValide = False
        self.estAnnule = False
        self.dateCreation = now

    def canCreateTable(hoteId, date, heure):

        dtString = str(date) + " " + str(heure) + str(".000")
        fullDate = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S.%f')        

        result = repositoryTable.canCreateTable(hoteId, fullDate)

        return result

    def createTable(form):
        dtString = str(form.date.data) + " " + str(form.heure.data) + str(".000")
        fullDate = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S.%f')

        hote = {"idJoueur": ObjectId(session['user']["idJoueur"]), "pseudo":  session["user"]["pseudo"]}
        table = Table(
            hote, 
            form.jeuxLibre.data, 
            form.nbPlace.data, 
            form.jeux.data, 
            fullDate, 
            session['user']["ville"], 
            form.ageMin.data, 
            form.age.data, 
            form.regle.data, 
            form.noteMin.data, 
            form.note.data)

        RepoTable.createTable(table)

    def findAvalaibleTable(idJoueur):
        result = RepoTable.findAvalaibleTable(idJoueur)

        return result

    def canJoinTable(table, joueur, note):

        ageCalcule = relativedelta(datetime.today(), joueur["dateDeNaissance"]).years
        
        if table["ageMin"] == True:
            if table["age"] >= ageCalcule:
                return False
        if table["noteMin"] == True:
                if table["note"] >= note:
                    return False
        if "joureurs" in table:
            if table["nbPlace"] == len(table["joueurs"]):
                return False

        return True
    

    def joinTable(joueur, idTable):
        repositoryTable.joinTable(joueur, idTable)


    def findTable(id):
        return  RepoTable.findTable(str(id))

    def findTableByPlayerAndValidity(id):
        return RepoTable.findTableByPlayerAndValidity(id)

    def findTableByHostAndValidity(id):
        return RepoTable.findTableByHostAndValidity(id)

    def saveTable(table):
        return RepoTable.saveTable(table)

    def findTableForNoteByIdJoueurAndPast(id):
        return RepoTable.findTableForNoteByIdJoueurAndPast(id)

    def getAllTables():
        return RepoTable.getAllTables()


    def findTableByDatePast():
        return RepoTable.findTableByDatePast()

    def findTableByDateFutur():
        return RepoTable.findTableByDateFutur()

    def closeTable(idTable):
        """joueur = RepoJoueur.findPlayerById(idJoueur)"""

        RepoTable.closeTable(idTable)  
        
        """RepoJoueur.updatePlayer(joueur)"""

class JeuxListeForm(Form):
    nom = StringField("", render_kw={"placeholder": "Nom"})
    version = StringField("", render_kw={"placeholder": "Version"})

class CreationTableForm(FlaskForm):

    from wtforms.fields import html5 as h5fields
    from wtforms.widgets import html5 as h5widgets

    jeuxLibre = BooleanField(' Jeux libre ?')
    nbPlace = IntegerField('', validators=[InputRequired()], render_kw={"placeholder": "Places libres"})
    jeux = FieldList(FormField(JeuxListeForm), min_entries=1,)
    date = DateField('', format='%Y-%m-%d', validators=[InputRequired()])
    heure = TimeField('', validators=[InputRequired()])
    ville = StringField('', render_kw={'disabled':''})
    ageMin = BooleanField('Définir un âge minimum ?')
    age = h5fields.IntegerField("", widget=h5widgets.NumberInput(min=15, max=100, step=1))
    regle = BooleanField(' Connaissance des règles requises ?')
    noteMin = BooleanField('Note minimum ?')
    note = IntegerRangeField('', default=0, render_kw={"placeholder": "Note"})

    def validate_nbPlace(self, nbPlace):
        if not isinstance(nbPlace.data, int):
            flash("indiquez un nombre!", "place")
            return ValidationError()
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

