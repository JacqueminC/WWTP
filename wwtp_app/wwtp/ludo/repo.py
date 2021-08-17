from pymongo import MongoClient
import pymongo
from bson import ObjectId
from bson.json_util import dumps
from pymongo.message import query


client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
ludoColl = db["ludo"]

class RepoLudo():

    def createLudo(self):
        ludoColl.insert_one(self.__dict__)

    def findLudoByPlayer(id):
        query = {
            "idJoueur" : ObjectId(id),
            "favori" : False
        }

        return ludoColl.find(query).sort([("nom", pymongo.ASCENDING)])

    def findLudoFavoriteByPlayer(id):
        query = {
            "idJoueur" : ObjectId(id),
            "favori" : True
        }

        return ludoColl.find(query).sort([("nom", pymongo.ASCENDING)])

    def deleteLudo(id):
        query = {
            "_id": ObjectId(id)
        }

        ludoColl.delete_one(query)

    def findLudoById(id):
        query = {
            "_id": ObjectId(id)
        }

        return ludoColl.find_one(query)

    def updateLudo(data):

        query = { "_id": data["_id"] }
        set = { "$set" : {"favori": data["favori"]} }

        ludoColl.update_one(query, set)

    