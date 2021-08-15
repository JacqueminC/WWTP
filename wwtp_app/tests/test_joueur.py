from hashlib import new
import pytest
from datetime import datetime, timedelta
import os

"""print("test")
print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))"""

from wwtp.joueur.model import Joueur

dateNow = datetime.today()

def test_new_player():
    try:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    except Exception as e:
        pytest.fail("Aucune erreur ne doit être retournéé - " + str(e))

    with pytest.raises(Exception) as e:
        joueur = Joueur("", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le pseudo ne doit pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail", "TestmotDePasse123", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "L'email n'est pas valide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarikgmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "L'email n'est pas valide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "test", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le mot de passe doit être de minimum 8 caratères" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le mot de passe doit contenir des chiffres" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "testmdp123", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le mot de passe doit contenir au moins une majuscule" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le nom ne doit pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le prénom ne doit pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "La rue ne doit pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", "10", "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le numéro de rue n'est pas valide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", 0, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "Le numéro de rue n'est pas valide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", 10, "b10", "", "1111", datetime(1988, 10, 8, 0,0,0))
    assert "La ville ne doit pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", 10, "b10", "city", "", datetime(1988, 10, 8, 0,0,0))
    assert "Le code postalne doit pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        joueur = Joueur("Cadarik", "cadarik@gmail.com", "TestmotDePasse123", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", dateNow - timedelta(weeks=780))
    assert "Il faut avoir au minimum 15 ans pour s'inscrire sur le site" in str(e.value)

def test_hash_and_verify_password():

    joueur = Joueur("Cadarik", "cadarik@gmail.com", "Gandalf06", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    result = Joueur.verifyPassword(joueur.motDePasse, "Gandalf06")
    assert result == True, "Le mot de passe doit matcher"

    joueur = Joueur("Cadarik", "cadarik@gmail.com", "Gandalf06", "nom", "prénom", "rue des rues", 10, "b10", "city", "1111", datetime(1988, 10, 8, 0,0,0))
    result = Joueur.verifyPassword(joueur.motDePasse, "Gandalf05")
    assert result == False, "Le mot de passe ne doit pas matcher"
    
    

def test_decrease_note():
    result = Joueur.decreaseNote(75, 100)
    assert result == 3.75, "La note est bonne, 3.75/5, il ne doit pas y avoir d'erreur !"

    result = Joueur.decreaseNote(41, 80)
    assert result != 2.56, "La note doit être arrondi à 2.56 !"

    result = Joueur.decreaseNote(75, 100)
    assert result > 0.00, "La note doit être supérieur à zéro !"

    result = Joueur.decreaseNote(75, 100)
    assert result < 5, "La note doit être inférieur ou égale à 5 !"


