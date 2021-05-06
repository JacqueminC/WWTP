from joueur.model import Joueur 

class Table:
    idTable = ""
    hote = Joueur("1", "toto")
    jeuxLibre = ""
    nbDePlaceLibre = 4
    date = ""
    ville = ""
    ageMin = 18
    regle = False
    noteMin = 0
    estValide = False

    def __init__(self, hote , jeuxLibre, nbDePlaceLibre, date, ville, ageMin, regle, noteMin, estValide):
        self.hote = hote
        self.jeuxLibre = jeuxLibre
        self.nbDePlaceLibre = nbDePlaceLibre
        self.date = date
        self.ville = ville
        self.ageMin = ageMin
        self.regle = regle
        self.noteMin = noteMin
        self.estValide = estValide


        