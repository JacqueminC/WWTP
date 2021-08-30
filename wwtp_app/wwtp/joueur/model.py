from flask import flash
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re, os, hashlib, smtplib
from wtforms.validators import InputRequired, ValidationError
from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, DateField
from wtforms import StringField, IntegerField, PasswordField, RadioField
from wtforms.fields.core import BooleanField


from pymongo.message import update

if __package__ == "wwtp.joueur":
    from wwtp.table.repo import RepoTable
else: 
    from table.repo import RepoTable

from .repo import *
from email.message import EmailMessage
from table.repo import RepoTable

class AccountForm(FlaskForm):
    nom = StringField("Nom", validators=[InputRequired()])
    prenom = StringField("Prénom", validators=[InputRequired()])
    rue = StringField("Rue", validators=[InputRequired()])
    numero = IntegerField("Numéro", validators=[InputRequired()])
    boite = StringField("Boite")
    codePostal = StringField("Code postal", validators=[InputRequired()])
    ville = StringField("Ville", validators=[InputRequired()])
    dateDeNaissance = DateField('Date de naissance', format='%Y-%m-%d', render_kw={'disabled':''})
    pseudo = StringField("Pseudo", render_kw={'disabled':''})
    email = EmailField("Email", render_kw={'disabled':''})
    mdp = PasswordField("", render_kw={'placeholder':'Nouveau mot de passe'})
    confMdp = PasswordField("", render_kw={'placeholder':'Nouveau mot de passe'})

class RegisterForm(FlaskForm):
    nom = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Nom"})
    prenom = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Prénom"})
    rue = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Rue"})
    numero = IntegerField("", validators=[InputRequired()], render_kw={"placeholder": "Numéro"})
    boite = StringField("", render_kw={"placeholder": "Boite"})
    codePostal = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Code postal"})
    ville = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Ville"})
    dateDeNaissance = DateField('Date de naissance', format='%Y-%m-%d', validators=[InputRequired()])
    pseudo = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Pseudo"})
    email = EmailField("", validators=[InputRequired()], render_kw={"placeholder": "Email"})
    motDePasse = PasswordField("", validators=[InputRequired()], render_kw={"placeholder": "Mot de passe"})
    confMDP = PasswordField("", validators=[InputRequired()], render_kw={"placeholder": "Confirmation du mot de passe"})

    def validate_dateDeNaissance(self, dateDeNaissance):
        now = datetime.today()
        ageCalcule = relativedelta(now, dateDeNaissance.data).years

        if ageCalcule < 15:
            flash("Il faut avoir 15 ans pour s'inscrire sur le site wtf", "ddn")
            return ValidationError()

    def validate_confMDP(self, confMDP):
        if confMDP.data != self.motDePasse.data:
            flash("La validation n'est pas correcte", "confmdp")
            return ValidationError()

    def validate_email(self, email):
        result = Joueur.findEmailExist(email.data)

        if result != 0:
            email.data = ""
            flash("L'email est déjà utilisé", "email")
            return ValidationError()

    def validate_pseudo(self, pseudo):
        p, find = Joueur.findPseudoExist(pseudo.data)

        if not find:
            pseudo.data = p
            flash("Le pseudo n'est pas disponible, essayé " + p, "pseudo")
            return ValidationError()


class AdminTable(FlaskForm):
    temps = RadioField('Label', choices=[('all','Tout'),('past','Passé'),('futur','Futur')], default='all')

class Joueur:

    def __init__(self, pseudo, email, motDePasse, nom, prenom, rue, numero, boite, ville, codePostal, dateDeNaissance):

        if len(pseudo) > 0:
            self.pseudo = pseudo
        else:
            raise Exception("Le pseudo ne doit pas être vide")

        if self.checkEmail(email):
            self.email =  email.lower()
        else:
            raise Exception("L'email n'est pas valide")
        
        if len(motDePasse) >= 8:           

            if self.hasNumbers(motDePasse):
                capital = bool(re.match(r'\w*[A-Z]\w*', motDePasse))

                if capital:
                    hash = Joueur.hashPassword(motDePasse)
                    self.motDePasse = hash
                else:
                    raise Exception("Le mot de passe doit contenir au moins une majuscule")
            else:
                raise Exception("Le mot de passe doit contenir des chiffres")
        else:
            raise Exception("Le mot de passe doit être de minimum 8 caratères")

        if len(nom) > 0:
            self.nom = nom
        else:
            raise Exception("Le nom ne doit pas être vide")

        if len(prenom) > 0:
            self.prenom = prenom
        else:
            raise Exception("Le prénom ne doit pas être vide")

        if len(rue) > 0:
            self.rue = rue
        else:
            raise Exception("La rue ne doit pas être vide")

        if isinstance(numero, int) and numero > 0:
            self.numero = numero
        else:
            raise Exception("Le numéro de rue n'est pas valide")

        self.boite = boite

        if len(ville) > 0:
            self.ville = ville
        else:
            raise Exception("La ville ne doit pas être vide")

        if len(str(codePostal)) > 0:
            self.codePostal = codePostal
        else:
            raise Exception("Le code postalne doit pas être vide")


        dateNow = date.today()

        ageCalcule = relativedelta(dateNow, dateDeNaissance).years


        if ageCalcule > 15:
            self.dateDeNaissance = dateDeNaissance
        else:
            raise  Exception("Il faut avoir au minimum 15 ans pour s'inscrire sur le siteeuh")

        self.dateDeCreation = datetime.today()
        self.estBloque = False

    def getAllPlayers():
        return RepoJoueur.getAllPlayers()

    def findPlayerById(id):
        return RepoJoueur.findPlayerById(id)

    def findEmailById(id):
        return RepoJoueur.findEmailById(id)

    def findPlayerByEmailAndAccess(email):
        return RepoJoueur.findPlayerByEmailAndAccess(email)

    def lockPlayer(id):
        RepoJoueur.lockPlayer(id)

    def decreaseNote(noteGlobale, max):
        average = (noteGlobale/max) * 5
        return round(average, 5)
    
    def joinTable(idJoueur, idTable):
        joueur = RepoJoueur.findPlayerById(idJoueur)
        RepoTable.joinTable(joueur, idTable)

    def leaveTable(idJoueur, idTable):
        RepoTable.leaveTable(idJoueur, idTable)
        

    def validateTable(idTable):
        RepoTable.validateTable(idTable)

    def sendMailCloseByPlayer(hote, table):

        subject = "Une table a été annulée"
        body = f"La table de {hote['pseudo']} du {table['date']} a été annulée !\n\nWWTP"
        emails = []        

        for joueur in table["joueurs"]:
            jEmail = Joueur.findEmailById(joueur["idJoueur"])            

            emails = emails + [jEmail["email"]]

        if len(emails) > 0:
            Joueur.sendEmail(emails, subject, body)

    def sendMailCloseByAdmin(id):

        table = RepoTable.findTable(id)
        hote = table["hote"]

        subject = "Une table a été annulée par un administrateur"
        body = f"La table de {hote['pseudo']} du {table['date']} a été annulée par un administrateur!\n\nWWTP"
        
        emails = []
        
        for joueur in table["joueurs"]:
            jEmail = Joueur.findEmailById(joueur["idJoueur"])
            

            emails = emails + [jEmail["email"]]

        if len(emails) > 0:
            Joueur.sendEmail(emails, subject, body)

    def sendEmail(emails, subject, body):
        msg = EmailMessage()
        msg.set_charset('utf8')
        msg['From'] = "wwtp.web.site@gmail.com"
        msg['To'] = emails
        msg['Subject'] = subject

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login("wwtp.web.site@gmail.com", "wflxfjxtwfseitvb")

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail("wwtp.web.site@gmail.com", emails, msg.encode('utf-8'))
 
    def checkEmail(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if(re.match(regex, email)):
            return True    
        else:
            return False
    
    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def hashPassword(mdp):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', mdp.encode('UTF-8'), salt, 100000)

        fullPwd = salt + key

        salt = fullPwd[:32]
        key = fullPwd[32:]

        return fullPwd.hex()

    def verifyPassword(hash, clearPwd):
        hashByte = bytes.fromhex(hash)

        salt = hashByte[:32]
        key = hashByte[32:]

        new_key = hashlib.pbkdf2_hmac('sha256', clearPwd.encode('utf-8'), salt, 100000)

        if new_key == key:
            return True
        else:
            return False

    def findEmailExist(email):
        return RepoJoueur.findEmailExist(email)


    def findPseudoExist(pseudo):
        result = RepoJoueur.findPseudoExist(pseudo)
        count = 0

        while result != 0:
            count = count + 1
            result = RepoJoueur.findPseudoExist(pseudo + str(count))

        if count == 0:
            return "", True
        else:
            return pseudo + str(count), False

    def createPlayer(form):
        fullDate = datetime.strptime(str(form.dateDeNaissance.data), '%Y-%m-%d')

        try:   
            joueur = Joueur(
                form.pseudo.data,
                str(form.email.data).lower(),
                form.motDePasse.data,
                form.nom.data,
                form.prenom.data,
                form.rue.data,
                form.numero.data,
                form.boite.data,
                form.ville.data,
                form.codePostal.data,
                fullDate
            )

            RepoJoueur.createPlayer(joueur)
        except Exception as ex:
            raise ex

    def updatePlayer(form, joueur):        

        try:
            joueur["nom"] = form.nom.data
            joueur["prenom"] = form.prenom.data 
            joueur["rue"] = form.rue.data 
            joueur["numero"] = form.numero.data
            joueur["boite"] = form.boite.data 
            joueur["codePostal"] = form.codePostal.data 
            joueur["ville"] = form.ville.data  

            value = str(form.mdp.data)
            if len(value) != 0:
                if form.mdp.data == form.confMdp.data:
                    if len(value) > 8:
                        if any(char.isdigit() for char in value):
                            capital = bool(re.match(r'\w*[A-Z]\w*', value))
                            if capital:
                                hash = Joueur.hashPassword(value)
                                joueur["motDePasse"] = hash
                            else:
                                raise Exception("Le mot de passe doit contenir au moins une majuscule")
                        else:
                            raise Exception("Le mot de passe doit contenir des chiffres")
                    else:
                        raise Exception("Le mot de passe doit être de minimum 8 caratères")                    
                else:
                    raise Exception("La confirmation du mot de passe n'est pas valide")            

            print("update")
            """RepoJoueur.updatePlayer(joueur)""" 
        except Exception as ex:
            raise ex

        
    

