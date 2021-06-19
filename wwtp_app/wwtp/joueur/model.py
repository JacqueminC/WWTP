from datetime import datetime

from werkzeug.datastructures import Headers
from wwtp.table.repo import RepoTable
from .repo import *
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.message import EmailMessage

repositoryTable = RepoTable()
repositoryJoueur = RepoJoueur()

class Joueur:

    def __init__(self, idJoueur, pseudo, email, motDePasse, nom, prenom, rue, numero, ville, codePostal, dateDeNaissance, note):
        self.idJoueur = idJoueur
        self.pseudo = pseudo
        self.email = email
        self.motDePasse = motDePasse
        self.nom = nom
        self.prenom = prenom
        self.rue = rue
        self.numero = numero
        self.ville = ville
        self.codePostal = codePostal
        self.dateDeNaissance = dateDeNaissance
        self.dateDeCreation = datetime.today()
        self.estBloque = False
        self.note = note
        self.noteGlobale = 0
        self.noteMax = 0

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
        joueur = RepoJoueur.findPlayerById(idJoueur)

        if "noteGlobale" in joueur:

            if joueur["noteGlobale"] >= 5:
                joueur["noteGlobale"] = joueur["noteGlobale"] - 5 
                note = Joueur.decreaseNote(joueur["noteGlobale"], joueur["noteMax"])
                joueur["note"] = note
            else:
                joueur["noteMax"] = joueur["noteMax"] + 5
                
            RepoJoueur.updatePlayer(joueur)

    def validateTable(idTable):
        RepoTable.validateTable(idTable)

    def closeTable(idTable, idJoueur, nbJoueurs):
        joueur = RepoJoueur.findPlayerById(idJoueur)
        table = RepoTable.findTable(idTable)

        RepoTable.closeTable(idTable)  

        if nbJoueurs != 0:
            nbJoueurs = nbJoueurs +1

        for j in range(nbJoueurs):
            if joueur["noteGlobale"] >= 5:
                joueur["noteGlobale"] = joueur["noteGlobale"] - 5 
                note = Joueur.decreaseNote(joueur["noteGlobale"], joueur["noteMax"])
                joueur["note"] = note
            else:
                joueur["noteMax"] = joueur["noteMax"] + 5
        
        RepoJoueur.updatePlayer(joueur)

    def sendEmail(emails, subject, body):
        print(emails)
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
    
            

