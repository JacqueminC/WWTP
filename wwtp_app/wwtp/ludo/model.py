from bson import ObjectId

class Ludo:

    def __init__(self, idJoueur, nom, version, minJ, maxJ, age, favori):
        if len(nom) > 0:
            self.nom = nom
        else:
            raise Exception("Le nom ne peut pas être vide")

        self.version = version

        if isinstance(idJoueur, ObjectId):
            self.idJoueur = idJoueur
        else:
            raise Exception("L'idJoueur doit être de type ObjectId")

        if isinstance(minJ, int):
            if minJ > 0:
                self.minJ = minJ
            else:
                raise Exception("Le minimum de joueur doit être de 1")
        else:
            raise Exception("Le minimum doit être un nombre")

        if isinstance(maxJ, int):
            if maxJ > 0:
                if maxJ >= minJ:
                    self.maxJ = maxJ
                else:
                    raise Exception("Le nombre maximum de joueur ne peut pas  être inférieur au nombre minimum de joueur")
        else:
            raise Exception("Le maximum doit être un nombre")

        if isinstance(age, int):
            self.age = age

        if isinstance(favori, bool):
            self.favori = favori
        else:
            raise Exception("Favori doit être un boolean")
    
    def get_favorite(self):
        return self.favorite

    def set_favorite(self, favorite):
        self.favorite = favorite