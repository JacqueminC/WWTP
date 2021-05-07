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

jeux = [jeu1, jeu2, jeu3]

dateBefore1 = datetime.today() - timedelta(days=60)
dateNow = datetime.today()
dateAfter1 = datetime.today() + timedelta(days=60)


def test_new_table():

    table1 = Table(joueur1, False, 5, jeux, dateAfter1, "La comté", 18, False, False)
    assert table1.jeuxLibre == False, "Jeux libre n'as pas été choisi"
    assert table1.nbDePlaceLibre >= 1, "Il doit y avoir au moins une place de libre"
    assert len(table1.jeux) >= 1, "Jeux libre n'est pas séléctionne la liste de jeu doit contenir au moins 1 jeu"
    for j in jeux:
        assert j.nom != None, "le nom du jeu ne peut pas être à None"
        assert j.nom != "", "le nom du jeu ne peut pas être vide"
        assert j.version != None, "la version du jeu ne peut pas être à None"
    
    assert table1.date >= datetime.today() + timedelta(hours=2), "La date de la table doit être à today() + 2h"
    assert table1.ville != "", "La ville ne peut pas être vide"
    
    table2 = Table(joueur1, True, 7, [], dateAfter1, "La comté", 18, False, False)
    assert table2.jeuxLibre == True, "Jeux libre as été choisi"
    assert table2.nbDePlaceLibre >= 1, "Il doit y avoir au moins une place de libre"
    assert len(table2.jeux) == 0, "Jeux libre est séléctionne la liste de jeu ne doit pas contenir de jeux"    
    assert table2.date >= datetime.today() + timedelta(hours=2), "La date de la table doit être à today() + 2h"
    assert table2.ville != "", "La ville ne peut pas être vide"

    #TODO generate bad var for test
    table3 = Table(joueur1, True, 7, jeux, dateNow, "La comté", 0, False, False)
    table4 = Table(joueur1, True, 7, jeux, dateBefore1, "La comté", 0, False, False)

