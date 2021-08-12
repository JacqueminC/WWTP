from datetime import datetime, timedelta
from pymongo import MongoClient, results
import pymongo
from bson import ObjectId
from pymongo.message import query

client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
evaluationColl = db["evaluation"]

class RepoEvaluation:

    def createEvaluation(eval):
        print("eval created")
        evaluationColl.insert_one(eval.__dict__)

    def CalculateNote(idJoueur):

        pipeline = [
            { "$match" : { "idJoueur": ObjectId(idJoueur) } },
            { "$group" : { 
                "_id": "$idJoueur", 
                "total": {"$sum": "$note"}, 
                "count" : { "$sum": 1 } } }
        ]

        result = evaluationColl.aggregate(pipeline)

        noteMoyenne = 0

        for doc in result:
            noteMoyenne = doc["total"] / (doc["count"])

        return noteMoyenne

    def findEvalByTable(id):

        query = {
            "idTable" : id,
            "info" : {"$ne": "leave"}
        }

        result = evaluationColl.find(query)

        return result

    def findNoteByEvaluateurAndEvalue(idEvaluateur, idEvalue, idTable):
        query = { "idEvaluateur": ObjectId(idEvaluateur), "idJoueur": ObjectId(idEvalue), "idTable" : ObjectId(idTable)}

        project = {"_id": 0, "note": 1}

        result = evaluationColl.find_one(query, project)

        return result 

        

