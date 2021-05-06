from joueur.model import Joueur 

class Table:
    idTable = ""
    jeuxLibre = ""
    nbDePlaceLibre = 4
    date = ""
    ville = ""
    ageMin = 18
    regle = False
    noteMin = 0

    def __init__(self, hote , jeuxLibre, nbDePlaceLibre, jeux, date, ville, ageMin, regle, noteMin):
        self.hote = hote
        self.jeuxLibre = jeuxLibre
        self.nbDePlaceLibre = nbDePlaceLibre
        self.jeux = jeux
        self.date = date
        self.ville = ville
        self.ageMin = ageMin
        self.regle = regle
        self.noteMin = noteMin




        