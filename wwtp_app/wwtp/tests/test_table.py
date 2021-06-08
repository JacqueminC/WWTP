from os import truncate
import pytest
from datetime import datetime, timedelta
from pymongo import MongoClient
from wwtp.table.model import Table
from wwtp.joueur.model import Joueur

dateBefore1 = datetime.today() - timedelta(days=60)
dateNow = datetime.today()
dateAfter1 = datetime.today() + timedelta(days=60)
datePlus7 = dateNow + timedelta(days=7)

joueur1 = {"1", "Bilbo", }
joueur2 = Joueur("Duke1", "Duke", "duke@gmail.com", "HASHPWD", "Duke", "Nukem", "rue Street", 10, "Mons", 7000, dateNow-timedelta(weeks=1040), 3)

jeu1 = {"Carcassonne", ""}
jeu2 = {"Catane", ""}
jeu3 = {"SmashUp", ""}

jeux1 = [jeu1, jeu2, jeu3]
jeux2 = []
jeux3 = None
client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
tableColl = db["table"]

def init_db_1():

    value = [{
            "test": "delete",
            "hote" : {
                "idJoueur": "Gandalf",
                "pseudo": "Test"
            },
            "jeuxLibre" : True,
            "nbPlace" : 4,
            "jeux" : [],
            "date" : datePlus7,
            "ville" : "La Louvière",
            "ageMin" : False,
            "regle" : False,
            "noteMin" : False
        },
        {
            "test": "delete",
            "hote" : {
                "idJoueur": "Bob",
                "pseudo": "Test"
            },
            "jeuxLibre" : True,
            "nbPlace" : 4,
            "jeux" : [],
            "date" : datePlus7,
            "ville" : "La Louvière",
            "ageMin" : False,
            "regle" : False,
            "noteMin" : False,
            "joueurs" : [{
                "idJoueur": "Lenon",
                "pseudo": "Test"
                }]
        }]

    tableColl.insert_many(value)

def init_db_2():
    value = [{
                "_id" : "test1",
                "test" : "delete",
                "count": "join",
                "hote" : {
                    "idJoueur": "Jimmy",
                    "pseudo": "Test"
                },
                "jeuxLibre" : True,
                "nbPlace" : 4,
                "jeux" : [],
                "date" : datePlus7,
                "ville" : "La Louvière",
                "ageMin" : True,
                "age" : 25,
                "regle" : False,
                "noteMin" : True,
                "note" : 3,
                "joueurs" : [{
                    "idJoueur": "Hendrickx",
                    "pseudo": "Test"
                    }]
            },
            {
                "_id" : "test2",
                "test": "delete",
                "count": "join",
                "hote" : {
                    "idJoueur": "Jimmy",
                    "pseudo": "Test"
                },
                "jeuxLibre" : True,
                "nbPlace" : 4,
                "jeux" : [],
                "date" : datePlus7,
                "ville" : "La Louvière",
                "ageMin" : False,
                "regle" : False,
                "noteMin" : True,
                "note" : 3,
                "joueurs" : [{
                    "idJoueur": "Hendrickx",
                    "pseudo": "Test"
                    }]
            },
            {
                "_id" : "test3",
                "test": "delete",
                "count": "join",
                "hote" : {
                    "idJoueur": "Jimmy",
                    "pseudo": "Test"
                },
                "jeuxLibre" : True,
                "nbPlace" : 4,
                "jeux" : [],
                "date" : datePlus7,
                "ville" : "La Louvière",
                "ageMin" : False,
                "regle" : False,
                "noteMin" : False,
                "joueurs" : [{
                    "idJoueur": "Hendrickx",
                    "pseudo": "Test"
                    }]
            },
            {
                "_id" : "test4",
                "test": "delete",
                "count": "join",
                "hote" : {
                    "idJoueur": "Jimmy",
                    "pseudo": "Test"
                },
                "jeuxLibre" : True,
                "nbPlace" : 4,
                "jeux" : [],
                "date" : datePlus7,
                "ville" : "La Louvière",
                "ageMin" : False,
                "regle" : False,
                "noteMin" : False,
                "joueurs" : [{
                    "idJoueur": "Hendrickx",
                    "pseudo": "Test"
                    },{
                    "idJoueur": "Duke1",
                    "pseudo": "Test"
                    }]
            }]

    tableColl.insert_many(value)

def clean_db():
    tableColl.delete_many({"test": "delete"})
    
def test_new_table(): 

    try:
        table1 = Table(joueur1, False, 4, jeux1, dateAfter1, "La comté", True, 18, False, False, 0)
    except Exception as e:
        pytest.fail("Aucune erreur ne doit être retourné - " + str(e))

    table1 = Table(joueur1, True, 5, jeux1, dateAfter1, "La comté", True, 18, False, False, 0)
    assert len(table1.jeux) == 0, "Jeux libre à été choisi, la liste ne doit pas être enregistrée"

    table1 = Table(joueur1, False, 5, jeux2, dateAfter1, "La comté", True, 18, False, False, 0)
    assert table1.jeuxLibre == True, "Aucun jeu n'a été encodé la table doit passer en jeux libre"

    with pytest.raises(Exception) as e:
        table1 = Table(joueur1, False, 5, jeux2, dateNow, "La comté", True, 18, False, False, 0)
    assert "La date ne peut pas être antérieur à la date actuelle PLUS 2h" in str(e.value)

    with pytest.raises(Exception) as e:
        table1 = Table(joueur1, False, 5, jeux2, dateAfter1, "", True, 18, False, False, 0)
    assert "La ville ne peut pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        table1 = Table(joueur1, False, 5, jeux2, dateAfter1, "Mons", True, 18, False, True, 6)
    assert "La note ne peut pas être suppérieur à 5 et inférieur à 0" in str(e.value)

    with pytest.raises(Exception) as e:
        table1 = Table(joueur1, False, 5, jeux2, dateAfter1, "Mons", True, 18, False, True, -1)
    assert "La note ne peut pas être suppérieur à 5 et inférieur à 0" in str(e.value)

    with pytest.raises(Exception) as e:
        table1 = Table(joueur1, False, 5, jeux2, dateAfter1, "Mons", True, 109, False, True, 5)
    assert "L'âge ne doit être compris entre 16 et 99" in str(e.value)

def test_canCreateTable():

    init_db_1()  
    try:
        dateTest1 = datePlus7 + timedelta(days=2)
        dateStr = str(dateTest1)

        result = Table.canCreateTable("Gandalf", dateStr[:10], dateStr[11:19])

        assert result == 0, "Une table peut être créée"

        dateTest2 = datePlus7 + timedelta(hours=4)
        dateStr = str(dateTest2)

        result = Table.canCreateTable("Gandalf", dateStr[:10], dateStr[11:19])

        assert result >= 1, "Une table ne doit pas être créée, l'hôte à déjà une table"

        result = Table.canCreateTable("Lenon", dateStr[:10], dateStr[11:19])

        assert result >= 1, "Une table ne doit pas être créée, l'hôte est joueur à une autre table"
    finally:
        clean_db()
    
def test_findAvalaibleTable():

    count = 0

    init_db_2()

    try:
        result = Table.findAvalaibleTable("Duke1")

        
        for r in result:
            print(r)
            if "count" in r:
                count += 1

        assert count == 3, "Trois Tables doivent être trouvées"
    finally:
        clean_db()

def test_canJoinTable():
    
    table1 = Table(joueur1, False, 4, jeux1, dateAfter1, "La comté", False, 0, False, False, 0)
    assert Table.canJoinTable(table1, joueur2) == True, "Le joueur peut rejoindre la table"

    table1 = Table(joueur1, False, 4, jeux1, dateAfter1, "La comté", True, 70, False, False, 0)
    assert Table.canJoinTable(table1, joueur2) == False, "Le joueur n'a pas l'age requis"

    table1 = Table(joueur1, False, 4, jeux1, dateAfter1, "La comté", False, 0, False, True, 4)
    assert Table.canJoinTable(table1, joueur2) == False, "Le joueur n'a pas une note suffisante"

    table1 = Table(joueur1, False, 4, jeux1, dateAfter1, "La comté", True, 70, False, True, 4)
    assert Table.canJoinTable(table1, joueur2) == False, "Le joueur n'a pas l'age requis et n'a pas une note suffisante"

