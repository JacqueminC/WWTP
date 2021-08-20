from bson.objectid import ObjectId
import pytest
from wwtp.ludo.model import Ludo

def test_create_ludo():
    try:
        ludo = Ludo(ObjectId(), "Catane", "Originale", 2, 4, 10, True)
    except Exception as e:
        pytest.fail("Aucune erreur ne doit être retournéé - " + str(e))

    with pytest.raises(Exception) as e:
        ludo = Ludo(ObjectId(), "", "Originale", 2, 4, 10, True)
    assert "Le nom ne peut pas être vide" in str(e.value)

    with pytest.raises(Exception) as e:
        ludo = Ludo("idJoueur0013320", "Catane", "Originale", 2, 4, 10, True)
    assert "L'idJoueur doit être de type ObjectId" in str(e.value)

    with pytest.raises(Exception) as e:
        ludo = Ludo(ObjectId(), "Catane", "Originale", 0, 4, 10, True)
    assert "Le minimum de joueur doit être de 1" in str(e.value)

    with pytest.raises(Exception) as e:
        ludo = Ludo(ObjectId(), "Catane", "Originale", 2, 1, 10, True)
    assert "Le nombre maximum de joueur ne peut pas  être inférieur au nombre minimum de joueur" in str(e.value)

    with pytest.raises(Exception) as e:
        ludo = Ludo(ObjectId(), "Catane", "Originale", "2", 4, 10, True)
    assert "Le minimum doit être un nombre" in str(e.value)

    with pytest.raises(Exception) as e:
        ludo = Ludo(ObjectId(), "Catane", "Originale", 2, "4", 10, True)
    assert "Le maximum doit être un nombre" in str(e.value)

    with pytest.raises(Exception) as e:
        ludo = Ludo(ObjectId(), "Catane", "Originale", 2, 4, 10, "True")
    assert "Favori doit être un boolean" in str(e.value)

def test_update_favorite():
    ludo = Ludo(ObjectId(), "Catane", "Originale", 2, 4, 10, False)
    ludo.set_favorite(True)
    assert ludo.get_favorite() == True, "Favorite n'a pas été modifié"

