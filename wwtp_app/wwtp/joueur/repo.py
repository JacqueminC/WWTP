from pymongo import MongoClient, results
import pymongo
from bson import ObjectId
from bson.json_util import dumps


client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
joueurColl = db["joueur"]

class RepoJoueur():

    def findPlayerById(idJoueur):
        query = {
            "_id" : ObjectId(idJoueur)
        }

        return joueurColl.find_one(query)