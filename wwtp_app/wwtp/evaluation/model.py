from .repo import *
from bson import ObjectId


repositoryEvaluation = RepoEvaluation()

class Evaluation:

    def __init__(self, idTable, idJoueur, idEvaluateur, note, info):
        if isinstance(note, int):
            if note <= 5:
                if note >=0:
                    self.note = note
                else:
                    raise Exception("La note ne doit pas être inférieur à 0 !")
            else:
                raise Exception("La note doit être inferieur à 5 !")  
        else:
            raise Exception("La valeur doit être un entier")

        if len(info.replace(" ","")) > 3:
            self.info = info
        else:
            raise Exception("Info doit contenir une valeur de 3 caractère minimum !")

        self.idTable = idTable
        self.idJoueur= idJoueur
        self.idEvaluateur = idEvaluateur

    def createEvaluation(idTable, idJoueur, idEvaluateur, note, info):
        eval = Evaluation(ObjectId(idTable), ObjectId(idJoueur), ObjectId(idEvaluateur), note, info)
        RepoEvaluation.createEvaluation(eval) 

    def calculateNote(idJoueur):
        result = RepoEvaluation.CalculateNote(idJoueur)
        return result

    def findEvalByTable(id):
        return RepoEvaluation.findEvalByTable(id)

    def findNoteByEvaluateurAndEvalue(idEvaluateur, idEvalue, idTable):
        return RepoEvaluation.findNoteByEvaluateurAndEvalue(idEvaluateur, idEvalue, idTable)