#print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))
from datetime import timedelta
from pymongo import MongoClient, results



#print("data.size => {0}".format(app.size))
#print("------------------------{0}".format(app.app.config["MONGO_URI"]))


client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
tableColl = db["table"]

class RepoTable:

    def FindCanCreateTable(hoteId, dateTable):
        print("date table " + str(dateTable))
        
        dateBefore = dateTable - timedelta(hours=8)
        dateAfter = dateTable + timedelta(hours=8)

        print("date table B " + str(dateBefore))
        print("date table A " + str(dateAfter))

        query1 = {"hoteId" : {"$elemMatch": {"joueurId": hoteId}}, 
            "date": {
                "$gte": dateBefore,
                "$lt": dateAfter
            }}

        result1 = tableColl.count_documents(query1)

        print("result 1 : " + str(result1))

        if result1 != 0:
            return result1

        query2 = {"joueurs": {"$elemMatch": {"joueurId": hoteId}},
            "date": {
                "$gte": dateBefore,
                "$lt": dateAfter
            }}

        result2 = tableColl.count_documents(query2)

        print("result 2 : " + str(result2))

        return result2

    def CreateTable(table):
        print(table.__dict__)
        result = tableColl.insert_one(table.__dict__)
        print("insert result : " + str(result))
        

    



