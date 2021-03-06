#print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))
from datetime import datetime, timedelta
from pymongo import MongoClient, results
import pymongo
from bson import ObjectId
from pymongo.message import query

client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
tableColl = db["table"]

class RepoTable:

    def getAllTables():
        return tableColl.find().sort([("date", pymongo.ASCENDING)])

    def findTableByDatePast():
        now = datetime.today()

        query = {
            "date" : {"$lte": now}
        }

        return tableColl.find(query)

    def findTableByDateFutur():
        now = datetime.today()

        query = {
            "date" : {"$gte": now}
        }

        return tableColl.find(query)

    def findTable(id):
        query = {
            "_id" : ObjectId(id)
        }

        return tableColl.find_one(query)

    def findTableByPlayerAndValidity(id):
        date = datetime.today() + timedelta(hours=2)

        query = {
            "joueurs.idJoueur": ObjectId(id),
            "estAnnule": False,
            "date": {"$gt": date}}

        return tableColl.find(query)

    def findTableByHostAndValidity(id):
        date = datetime.today() + timedelta(hours=2)

        query = {
            "hote.idJoueur": ObjectId(id), 
            "date": {"$gt": date}}

        return tableColl.find(query)

    def isHote(self, hoteId, dateTable):
        
        dateBefore = dateTable - timedelta(hours=8)
        dateAfter = dateTable + timedelta(hours=8)

        query = {"hote.idJoueur": ObjectId(hoteId), 
            "date": {
                "$gte": dateBefore,
                "$lt": dateAfter
            }}

        return tableColl.count_documents(query)

    def isPlayer(self, hoteId, dateTable):

        dateBefore = dateTable - timedelta(hours=8)
        dateAfter = dateTable + timedelta(hours=8)

        query = {"joueurs": {"$elemMatch": {"idJoueur": ObjectId(hoteId)}},
            "date": {
                "$gte": dateBefore,
                "$lt": dateAfter
            }}

        return tableColl.count_documents(query)

    def canCreateTable(self, hoteId, dateTable):

        result = self.isHote(hoteId, dateTable)

        if result > 0:
            return result
        else:
            result = self.isPlayer(hoteId, dateTable)
            return result 

    def findAvalaibleTable(idJoueur):

        now = datetime.today()

        query = {
            "hote.idJoueur" : {"$ne" : ObjectId(idJoueur)},
            "joueurs.idJoueur" : {"$ne": ObjectId(idJoueur)},
            "estValide" : False,
            "estAnnule" : False,
            "date" : {
                "$gte": now
            }
        }

        sort = {
            "date": -1
        }

        result = tableColl.find(query).sort([("date", pymongo.ASCENDING)])

        return result

    def createTable(table):
        tableColl.insert_one(table.__dict__)

    def joinTable(joueur, idTable):
        find = {"_id" : ObjectId(idTable)}
        push = {"$push": {"joueurs": {"idJoueur": ObjectId(joueur["_id"]), "pseudo": joueur["pseudo"]}}}

        tableColl.update_one(find, push)

    def leaveTable(idJoueur, idTable):
        find = {"_id" : ObjectId(idTable)}
        pull = {"$pull": {"joueurs" : {"idJoueur": ObjectId(idJoueur)}}}
        
        tableColl.update_one(find, pull)

    def validateTable(idTable):
        find = {"_id" : ObjectId(idTable)}
        save = {"$set" : {"estValide": True, "dateValide": datetime.today()}}

        tableColl.update(find, save)
    
    def closeTable(idTable):
        find = {"_id" : ObjectId(idTable)}
        save = {"$set" : {"estAnnule": True, "dateAnnule": datetime.today()}}

        tableColl.update(find, save)

    def findTableForNoteByIdJoueurAndPast(id):
        now = datetime.today()

        query = {"$or" : [{"hote.idJoueur": ObjectId(id)}, {"joueurs.idJoueur": ObjectId(id)}], 
                "date": {"$gte": now - timedelta(days=60), "$lte": now - timedelta(hours=12) },
                "estValide": True, "estAnnule": False}

        result = tableColl.find(query).sort([("date", pymongo.ASCENDING)])

        return result





    



        

    



