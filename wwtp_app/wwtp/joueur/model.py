from datetime import datetime
from wwtp.table.repo import *
from .repo import *
import math

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

    def decreaseNote(noteGlobale, max):
        average = (noteGlobale/max) * 5
        print(type(round(average, 5)))
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

