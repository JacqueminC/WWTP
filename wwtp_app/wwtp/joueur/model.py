from datetime import datetime
from itertools import count
from attr import has
from dateutil.relativedelta import relativedelta
from wwtp.table.repo import RepoTable
from .repo import *
from email.message import EmailMessage
import re, os, hashlib, smtplib
import base64

repositoryTable = RepoTable()
repositoryJoueur = RepoJoueur()

class Joueur:

    def __init__(self, pseudo, email, motDePasse, nom, prenom, rue, numero, boite, ville, codePostal, dateDeNaissance):

        if len(pseudo) > 0:
            self.pseudo = pseudo
        else:
            raise Exception("Le pseudo ne doit pas être vide")

        if self.checkEmail(email):
            self.email = email
        else:
            raise Exception("L'email n'est pas valide")
        
        if len(motDePasse) > 0:               

            if self.hasNumbers(motDePasse):
                capital = bool(re.match(r'\w*[A-Z]\w*', motDePasse))

                if capital:
                    hash = self.hashPassword(motDePasse)
                    self.motDePasse = hash
                else:
                    raise Exception("Le mot de passe doit contenir au moins une majuscule")
            else:
                raise Exception("Le mot de passe doit contenir des chiffres")

        else:
            raise Exception("Le mot de passe ne doit pas être vide")

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

        dateNow = datetime.today()
        ageCalcule = relativedelta(dateNow, dateDeNaissance).years

        if ageCalcule > 15:
            self.dateDeNaissance = dateDeNaissance
        else:
            raise  Exception("Il faut avoir au minimum 15 ans pour s'inscrire sur le site")

        self.dateDeCreation = datetime.today()
        self.estBloque = False

    def findPlayerById(id):
        return RepoJoueur.findPlayerById(id)

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

    def closeTable(idTable, idJoueur, nbJoueurs):
        joueur = RepoJoueur.findPlayerById(idJoueur)

        RepoTable.closeTable(idTable)  
        
        RepoJoueur.updatePlayer(joueur)

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


    def hashPassword(self, mdp):
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
            return pseudo
        else:
            return pseudo + str(count)

    def createPlayer(form):
        """"pseudo, email, motDePasse, nom, prenom, rue, numero, boite, ville, codePostal, dateDeNaissance"""
        try:
            joueur = Joueur(
                form.pseudo,
                form.email,
                form.motDePasse,
                form.nom,
                form.prenom,
                form.rue,
                form.numero,
                form.boite,
                form.ville,
                form.codePostal,
                form.dateDeNaissance
            )

            RepoJoueur.createPlayer(joueur)
        except Exception as ex:
            return ex



