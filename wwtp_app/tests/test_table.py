import pytest
from datetime import date, datetime, timedelta
from table import table
from table.model import Table
from joueur.model import Joueur
from jeu.model import Jeu

joueur1 = Joueur("1", "Bilbo")


jeu1 = Jeu("Carcassonne", "")
jeu2 = Jeu("Catane", "")
jeu3 = Jeu("SmashUp", "")

jeux1 = [jeu1, jeu2, jeu3]
jeux2 = []
jeux3 = None

dateBefore1 = datetime.today() - timedelta(days=60)
dateNow = datetime.today()
dateAfter1 = datetime.today() + timedelta(days=60)


def test_new_table(): 
    #TODO generate bad var for test

    try:
        table1 = Table(joueur1, False, 4, jeux1, dateAfter1, "La comté", 18, False, False)
    except Exception as e:
        pytest.fail("Aucune erreur ne doit être retourné - " + str(e))

    
    table1 = Table(joueur1, True, 5, jeux1, dateAfter1, "La comté", 18, False, False)
    assert table1.jeux == None, "Jeux libre à été choisi, la liste ne doit pas être enregistrée"

    table1 = Table(joueur1, False, 5, jeux2, dateAfter1, "La comté", 18, False, False)
    assert table1.jeuxLibre == True, "Aucun jeu n'a été encodé la table doit passer en jeux libre"

    with pytest.raises(Exception) as e:
        table1 = Table(joueur1, False, 5, jeux2, dateNow, "La comté", 18, False, False)
    assert "La date ne peut pas être antérieur à la date actuelle PLUS 2h" in str(e.value)

    with pytest.raises(Exception) as e:
        table1 = Table(joueur1, False, 5, jeux2, dateAfter1, "", 18, False, False)
    assert "La ville ne peut pas être vide" in str(e.value)



