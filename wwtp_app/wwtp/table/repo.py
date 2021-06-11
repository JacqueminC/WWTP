#print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))
from datetime import datetime, timedelta
from pymongo import MongoClient, results
import pymongo
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
tableColl = db["table"]

class RepoTable:

    def findTable(id):

        query = {
            "_id" : ObjectId(id)
        }

        return tableColl.find_one(query)

    def saveTable(table):
        return tableColl.save(table)

    def isHote(self, hoteId, dateTable):
        
        dateBefore = dateTable - timedelta(hours=8)
        dateAfter = dateTable + timedelta(hours=8)

        print(dateBefore)
        print(dateAfter)

        query = {"hote.idJoueur": hoteId, 
            "date": {
                "$gte": dateBefore,
                "$lt": dateAfter
            }}

        return tableColl.count_documents(query)

    def isPlayer(self, hoteId, dateTable):

        dateBefore = dateTable - timedelta(hours=8)
        dateAfter = dateTable + timedelta(hours=8)

        print(dateBefore)
        print(dateAfter)

        query = {"joueurs": {"$elemMatch": {"idJoueur": hoteId}},
            "date": {
                "$gte": dateBefore,
                "$lt": dateAfter
            }}

        return tableColl.count_documents(query)

    def canCreateTable(self, hoteId, dateTable):

        result = self.isHote(hoteId, dateTable)

        print(result)

        if result > 0:
            return result
        else:
            result = self.isPlayer(hoteId, dateTable)
            print(result)
            return result 

    def findAvalaibleTable(idJoueur):

        now = datetime.today()

        print(idJoueur)

        query = {
            "hote.idJoueur" : {"$ne" : idJoueur},
            "joueurs.idJoueur" : {"$ne": idJoueur},
            "date" : {
                "$gte": now
            }
        }

        print(query)

        sort = {
            "date": -1
        }

        result = tableColl.find(query).sort([("date", pymongo.ASCENDING)])

        return result

    def createTable(table):
        tableColl.insert_one(table.__dict__)

    def joinTable(joueur, idTable):

        find = {"_id" : idTable}
        push = {"$push": {"joueurs": {"idJoueur": joueur.idJoueur, "nom": joueur.nom, "pseudo" : joueur.pseudo}}}

        tableColl.update_one(find, push)

    



        

    



