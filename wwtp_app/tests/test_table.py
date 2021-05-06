import pytest
from datetime import date, datetime, timedelta
from table import table
from table.model import Table
from joueur.model import Joueur
from jeu.model import Jeu

joueur1 = Joueur("1", "Bilbo")
joueur2 = Joueur("2", "Frodo")
joueur3 = Joueur("3", "Gandalf")
joueur4 = Joueur("4", "Gimli")
joueur5 = Joueur("5", "Legolas")
joueur6 = Joueur("6", "Aragorn")


jeu1 = Jeu("Carcassonne", "", 4)
jeu2 = Jeu("Catane", "", 3)
jeu3 = Jeu("SmashUp", "", 3)

jeux = [jeu1, jeu2, jeu3]

dateAfter1 = date.today() - timedelta(60)
dateNow = date.today()
dateBefore1 = date.today() + timedelta(60)


#TODO generate good var for test
#TODO generate bad var for test

def test_method():
    assert table.tableForm() == True