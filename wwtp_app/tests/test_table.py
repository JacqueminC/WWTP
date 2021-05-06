import pytest
from datetime import date, datetime, timedelta
from table import table
from table.model import Table
from joueur.model import Joueur
from jeu.model import Jeu

joueur1 = Joueur("1", "Bilbo")


jeu1 = Jeu("Carcassonne", "", 4)
jeu2 = Jeu("Catane", "", 3)
jeu3 = Jeu("SmashUp", "", 3)

jeux = [jeu1, jeu2, jeu3]

dateBefore1 = date.today() - timedelta(60)
dateNow = date.today()
dateAfter1 = date.today() + timedelta(60)


#TODO generate good var for test
table1 = Table(joueur1, False, 0, jeux, dateAfter1, "La comté", 18, False, False)
table2 = Table(joueur1, True, 7, [], dateAfter1, "La comté", 18, False, False)

#TODO generate bad var for test
table3 = Table(joueur1, True, 7, jeux, dateNow, "La comté", 0, False, False)
table3 = Table(joueur1, True, 7, jeux, dateBefore1, "La comté", 0, False, False)

def test_method():
    assert table.tableForm() == True