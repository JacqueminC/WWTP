from datetime import datetime
from wwtp.table.repo import *
from .repo import *

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

    
    def joinTable(idJoueur, idTable):

        joueur = RepoJoueur.findPlayerById(idJoueur)
        RepoTable.joinTable(joueur, idTable)
