from joueur.model import Joueur
from datetime import date, datetime, timedelta

class Table:

    def __init__(self, hote , jeuxLibre, nbPlace, jeux, date, ville, ageMin, regle, noteMin):
        self.hote = hote
        self.jeuxLibre = jeuxLibre

        if nbPlace < 1:
            raise Exception("Il doit y avoir au moins une place de libre")
        else:
            self.nbPlace = nbPlace
        
        if jeuxLibre == True:
            del jeux[:]
            self.jeux = jeux
        elif jeuxLibre == False and len(jeux) < 1:
            self.jeuxLibre = True
        else:
            self.jeux = jeux

        self.jeux = jeux

        if date < datetime.today() + timedelta(hours=2):
            raise Exception("La date ne peut pas être antérieur à la date actuelle PLUS 2h")
        else:
            self.date = date            
        
        if ville == "" or ville == None:
            raise Exception("La ville ne peut pas être vide")
        else:
            self.ville = ville

        self.ageMin = ageMin
        self.regle = regle
        self.noteMin = noteMin




        