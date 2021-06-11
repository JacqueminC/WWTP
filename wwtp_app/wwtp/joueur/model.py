from datetime import datetime


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
        self.note = 0
        self.dateDeCreation = datetime.today()
        self.estBloque = False
        self.note = note
