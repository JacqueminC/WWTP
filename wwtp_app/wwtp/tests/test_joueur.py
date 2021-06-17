import pytest
from pymongo import MongoClient
from wwtp.joueur.model import Joueur

client = MongoClient('mongodb://localhost:27017/')
db = client["wwtp"]
tableColl = db["joueur"]

def test_decrease_note():
    result = Joueur.decreaseNote(75, 100)
    assert result == 3.75, "La note est bonne, 3.75/5, il ne doit pas y avoir d'erreur !"

    result = Joueur.decreaseNote(41, 80)
    assert result != 2.56, "La note doit être arrondi à 2.56 !"

    result = Joueur.decreaseNote(75, 100)
    assert result > 0.00, "La note doit être supérieur à zéro !"

    result = Joueur.decreaseNote(75, 100)
    assert result < 5, "La note doit être inférieur ou égale à 5 !"
