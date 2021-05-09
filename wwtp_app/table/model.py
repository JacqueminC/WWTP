from joueur.model import Joueur 

class Table:
    idTable = ""
    #jeuxLibre True pour jeux libre ou False pour jeux prédéfini
    nbPlace = 4
    date = ""
    ville = ""
    ageMin = 18
    regle = False
    noteMin = 0

    def __init__(self, hote , jeuxLibre, nbPlace, jeux, date, ville, ageMin, regle, noteMin):
        self.hote = hote
        self.jeuxLibre = jeuxLibre

        if nbPlace < 1:
            raise Exception("Il doit y avoir au moins une place de libre")
        else:
            self.nbPlace = nbPlace
        
        if jeuxLibre == True:
            self.jeux = None
        elif jeuxLibre == False and len(jeux) < 1:
            self.jeuxLibre == True
        else:
            self.jeux = jeux

        self.jeux = jeux
        self.date = date
        self.ville = ville
        self.ageMin = ageMin
        self.regle = regle
        self.noteMin = noteMin




        