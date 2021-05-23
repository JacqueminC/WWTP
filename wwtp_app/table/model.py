from joueur.model import Joueur
from table.repo import RepoTable
from datetime import datetime, timedelta

class Table:

    def __init__(self, hote , jeuxLibre, nbPlace, jeux, date, ville, ageMin, regle, noteMin):
        self.hote = hote

        if isinstance(jeuxLibre, bool):
            self.jeuxLibre = jeuxLibre
        else:
            raise Exception("Le format de jeuxLibre n'est pas un boolean")


        if nbPlace < 1:
            raise Exception("Il doit y avoir au moins une place de libre")
        else:
            self.nbPlace = nbPlace

        if isinstance(jeuxLibre, bool):
            if jeuxLibre == True:
                self.jeux = list()
            elif jeuxLibre == False and len(jeux) < 1:
                self.jeuxLibre = True
            else:
                self.jeux = jeux
        else:
            raise Exception("Le format de jeuxLibre n'est pas un boolean")
            

        if date < datetime.today() + timedelta(hours=2):
            raise Exception("La date ne peut pas être antérieur à la date actuelle PLUS 2h")
        else:
            if isinstance(date, datetime):
                self.date = date
            else:
                raise Exception("Le format de la date n'est pas une string")          
        
        if ville == "" or ville == None:
            raise Exception("La ville ne peut pas être vide")
        else:
            if isinstance(ville, str):
                self.ville = ville
            else:
                raise Exception("Le format de la ville n'est pas une string")

        if isinstance(ageMin, int):
            self.ageMin = ageMin
        else:
            raise Exception("Le format de l'ageMin n'est pas un in")

        if isinstance(regle, bool):
            self.regle = regle
        else:
            raise Exception("Le format de regle n'est pas un boolean")
        self.noteMin = noteMin

    def canCreateTable():
        #est-ce que l'hote peut créer cette table?
        #n'est il pas déjà inscrit sur une autre table comme hote ou joueur à - ou + de 8h
        r = RepoTable.FindAll()
        return r