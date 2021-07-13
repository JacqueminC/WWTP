from datetime import datetime
from werkzeug.datastructures import Headers
from wwtp.table.repo import RepoTable
from .repo import *
import smtplib
from email.message import EmailMessage

repositoryTable = RepoTable()
repositoryJoueur = RepoJoueur()

class Joueur:

    def __init__(self, pseudo, email, motDePasse, nom, prenom, rue, numero, boite, ville, codePostal, dateDeNaissance):
        self.pseudo = pseudo
        self.email = email
        self.motDePasse = motDePasse
        self.nom = nom
        self.prenom = prenom
        self.rue = rue
        self.numero = numero
        self.boite = boite
        self.ville = ville
        self.codePostal = codePostal
        self.dateDeNaissance = dateDeNaissance
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
    
            

