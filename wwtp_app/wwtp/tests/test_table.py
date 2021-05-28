import pytest
from datetime import datetime, timedelta
from pymongo import MongoClient
from wwtp.table.model import Table

joueur1 = {"1", "Bilbo"}

jeu1 = {"Carcassonne", ""}
jeu2 = {"Catane", ""}
jeu3 = {"SmashUp", ""}

jeux1 = [jeu1, jeu2, jeu3]
jeux2 = []
jeux3 = None

dateBefore1 = datetime.today() - timedelta(days=60)
dateNow = datetime.today()
dateAfter1 = datetime.today() + timedelta(days=60)


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
    client = MongoClient('mongodb://localhost:27017/')
    db = client["tests"]
    tableColl = db["table"]

    dtString = "2021-05-28 10:00:00.000"
    fullDate = datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S.%f')

    value = [{
        "hoteId" : 1,
        "jeuxLibre" : True,
        "nbPlace" : 4,
        "jeux" : [],
        "date" : fullDate,
        "ville" : "La Louvière",
        "ageMin" : False,
        "regle" : False,
        "noteMin" : False
        }]

    print("----------------")

    tableColl.insert_many(value)

    result = Table.canCreateTable(1, "2021-05-30", "10:00:00")

    assert result == 0, "Une table peut être créée"

    result = Table.canCreateTable(1, "2021-05-28", "04:00:00")

    print("test ------------------------ : " + str(result))

    assert result >= 1, "Une table ne doit pas être créée"





