from datetime import datetime, timedelta
from pymongo import MongoClient, results
import pymongo
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
evaluationColl = db["evaluation"]

class RepoEvaluation:

    def createEvaluation(eval):
        evaluationColl.insert_one(eval.__dict__)

    def CalculateNote(idJoueur):

        query = {
            "idJoueur": ObjectId(idJoueur)
        }

        sumEval = evaluationColl.count_documents(query)

        pipeline = [
            { "$match" : { "idJoueur": ObjectId(idJoueur) } },
            { "$group" : { 
                "_id": "$idJoueur", 
                "total": {"$sum": "$note"}, 
                "count" : { "$sum": 1 } } }
        ]

        result = evaluationColl.aggregate(pipeline)

        for doc in result:
            noteMoyenne = doc["total"] / (doc["count"])

        return noteMoyenne

        

