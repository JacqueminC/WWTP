from wwtp.joueur.model import Joueur
from .repo import *
from datetime import datetime, timedelta
import json


class Table:

    def __init__(self, hote , jeuxLibre, nbPlace, jeux, date, ville, ageMin, age, regle, noteMin, note):
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

        if isinstance(ageMin, bool):
            self.ageMin = ageMin
        else:
            raise Exception("Le format de l'ageMin n'est pas un boolean")

        if ageMin == True:
            if isinstance(age, int):
                if age >= 16 and age <= 99:
                    self.age = age
                else:
                    raise Exception("L'âge ne doit être compris entre 16 et 99")
            else:
                raise Exception("Le format de l'age n'est pas un integer")  

        if isinstance(regle, bool):
            self.regle = regle
        else:
            raise Exception("Le format de regle n'est pas un boolean")

        self.noteMin = noteMin

        if noteMin == True:
            if isinstance(note, int):
                if note >= 0 and note <= 5:
                    self.note = note
                else:
                    raise Exception("La note ne peut pas être suppérieur à 5 et inférieur à 0")
            else:
                raise Exception("La note doit être un integer")

        self.joueurs = []

    def canCreateTable(hoteId, date, heure):

        dtString = str(date) + " " + str(heure) + str(".000")
        fullDate = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S.%f')

        print(fullDate)

        result = RepoTable.FindCanCreateTable(hoteId, fullDate)

        return result

    def createTable(form):
        dtString = str(form.date.data) + " " + str(form.heure.data) + str(".000")
        fullDate = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S.%f')

        """json.dumps(hote.__dict__, ensure_ascii=False)"""
        hote = Joueur(1, "Cédric")
        table = Table(
            hote.__dict__, 
            form.jeuxLibre.data, 
            form.nbPlace.data, 
            form.jeux.data, 
            fullDate, 
            form.ville.data, 
            form.ageMin.data, 
            form.age.data, 
            form.regle.data, 
            form.noteMin.data, 
            form.age.data)
        
        RepoTable.CreateTable(table)