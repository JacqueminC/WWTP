import pytest
from wwtp.evaluation.model import Evaluation

def test_createNote():

    try:
        """idTable, idJoueur, idEvaluateur, note, info"""
        evaluation = Evaluation("idTable001", "idjoueur001", "idEvaluateur001", 5, "test")
    except Exception as e:
        pytest.fail("Aucune exception ne doit être retournée - " + str(e))

    with pytest.raises(Exception) as e:
        evaluation = Evaluation("idTable001", "idjoueur001", "idEvaluateur001", 6, "test")
    assert "La note doit être inferieur à 5 !" in str(e.value)
    
    with pytest.raises(Exception) as e:
        evaluation = Evaluation("idTable001", "idjoueur001", "idEvaluateur001", -1, "test")
    assert "La note ne doit pas être inférieur à 0 !" in str(e.value)

    with pytest.raises(Exception) as e:
        evaluation = Evaluation("idTable001", "idjoueur001", "idEvaluateur001", 1.5, "test")
    assert "La valeur doit être un entier" in str(e.value)

    with pytest.raises(Exception) as e:
        evaluation = Evaluation("idTable001", "idjoueur001", "idEvaluateur001", 3, "")
    assert "Info doit contenir une valeur de 3 caractère minimum !" in str(e.value)
