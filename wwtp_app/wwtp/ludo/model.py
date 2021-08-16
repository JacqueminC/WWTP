from bson import ObjectId
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, ValidationError

class GameForm(FlaskForm):
    nom = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Nom"})
    version = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Version"})
    min = IntegerField("", validators=[InputRequired(IntegerField)], render_kw={"placeholder": "min"})
    max = IntegerField("", validators=[InputRequired()], render_kw={"placeholder": "max"})
    age = IntegerField("", validators=[InputRequired()], render_kw={"placeholder": "Age"})
    favori = BooleanField("Favori")

    def validate_nom(self, nom):
        if len(nom.data) < 1:
            flash("Le nom ne doit pas être vide", "error")
            return ValidationError()

    def validate_version(self, version):
        if len(version.data) < 1:
            flash("La version ne doit pas être vide", "error")
            return ValidationError()

    def validate_min(self, min):
        print("test")
        if min.data < 1:
            flash("Min doit être supérieur à zéro", "error")
            return ValidationError()
        elif self.max.data < min.data:
            flash("Max ne doit pas être plus petit que min", "error")
            return ValidationError()

        return super().validate_on_submit()


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