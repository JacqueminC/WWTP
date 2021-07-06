from .repo import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import session

repositoryTable = RepoTable()

class Table:

    def __init__(self, hote , jeuxLibre, nbPlace, jeux, date, ville, ageMin, age, regle, noteMin, note):
        now = datetime.today()

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
        self.estValide = False
        self.estAnnule = False
        self.dateCreation = now

    def canCreateTable(hoteId, date, heure):

        dtString = str(date) + " " + str(heure) + str(".000")
        fullDate = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S.%f')        

        result = repositoryTable.canCreateTable(hoteId, fullDate)

        return result

    def createTable(form):
        dtString = str(form.date.data) + " " + str(form.heure.data) + str(".000")
        fullDate = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S.%f')

        hote = {"idJoueur": ObjectId(session['user']['idJoueur']), "nom":  session['user']['nom']}
        table = Table(
            hote, 
            form.jeuxLibre.data, 
            form.nbPlace.data, 
            form.jeux.data, 
            fullDate, 
            form.ville.data, 
            form.ageMin.data, 
            form.age.data, 
            form.regle.data, 
            form.noteMin.data, 
            form.note.data)

        RepoTable.createTable(table)

    def findAvalaibleTable(idJoueur):
        result = RepoTable.findAvalaibleTable(idJoueur)
        return result

    def canJoinTable(table, joueur):

        dtFormat = datetime.strptime(joueur["dateDeNaissance"].strftime('%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S.%f')

        ageCalcule = relativedelta(datetime.today(), dtFormat).years        
        
        if table["ageMin"] == True:
            if table["age"] >= ageCalcule:
                return False
        if table["noteMin"] == True:
            if table["note"] >= joueur["note"]:
                return False
        if "joureurs" in table:
            if table["nbPlace"] == len(table["joueurs"]):
                return False

        return True

    def joinTable(joueur, idTable):
        repositoryTable.joinTable(joueur, idTable)


    def findTable(id):
        return  RepoTable.findTable(str(id))

    def findTableByPlayer(id):
        return RepoTable.findTableByPlayer(id)

    def findTableByHost(id):
        return RepoTable.findTableByHost(id)

    def saveTable(table):
        return RepoTable.saveTable(table)

    def findTableForNoteByIdJoueurAndPast(id):
        return RepoTable.findTableForNoteByIdJoueurAndPast(id)

