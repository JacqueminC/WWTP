from pymongo import MongoClient, results
import pymongo
from bson import ObjectId
from bson.json_util import dumps
from pymongo.message import query


client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
joueurColl = db["joueur"]

class RepoJoueur():

    def findPlayerById(idJoueur):
        query = {
            "_id" : ObjectId(idJoueur)
        }

        return joueurColl.find_one(query)

    def findPlayerByEmailAndAccess(email):
        query = {
            "email" : email,
            "estBloque": False
        }

        return joueurColl.find_one(query)

    def findEmailById(id):
        query = {
            "_id" : ObjectId(id)
            }
        project = {"_id": 0, "email": 1}

        return joueurColl.find_one(query, project)

    def updatePlayer(joueur):
        joueurColl.save(joueur)

    def findEmailExist(email):
        query = {
            "email" : email
        }

        return joueurColl.count_documents(query)

    def findPseudoExist(pseudo):
        query = {
            "pseudo" : pseudo
        }

        return joueurColl.count_documents(query)

    def createPlayer(joueur):
        joueurColl.insert_one(joueur.__dict__)