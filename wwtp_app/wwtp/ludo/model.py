from bson import ObjectId
from flask.helpers import flash
from flask.templating import render_template
from flask.wrappers import Response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, ValidationError
from .repo import RepoLudo
from requests import get
import requests
import json
import xml.etree.ElementTree as ET

repo = RepoLudo()

class GameForm(FlaskForm):
    nom = StringField("", validators=[InputRequired()], render_kw={"placeholder": "Nom"})
    version = StringField("", render_kw={"placeholder": "Version"})
    min = IntegerField("", validators=[InputRequired(IntegerField)], render_kw={"placeholder": "min"})
    max = IntegerField("", validators=[InputRequired()], render_kw={"placeholder": "max"})
    age = IntegerField("", validators=[InputRequired()], render_kw={"placeholder": "Age"})
    favori = BooleanField("Favori")

    def validate_nom(self, nom):
        if len(nom.data) < 1:
            flash("Le nom ne doit pas être vide", "error")
            return ValidationError()

    def validate_min(self, min):
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

    def createLudo(self):
        RepoLudo.createLudo(self)

    def findLudoByPlayer(id):
        return RepoLudo.findLudoByPlayer(id)

    def findLudoFavoriteByPlayer(id):
        return RepoLudo.findLudoFavoriteByPlayer(id)
    
    def deleteLudo(id):
        RepoLudo.deleteLudo(id)

    def updateFavorite(id):
        r = RepoLudo.findLudoById(id)

        if r["favori"] == True:
            r["favori"] = False
        else:
            r["favori"] = True

        RepoLudo.updateLudo(r)

    def findOnBGG(game):  
        print("start")      
        url = 'https://www.boardgamegeek.com/xmlapi/search?search='
        urlGame = "https://www.boardgamegeek.com/xmlapi/boardgame/"
        r = get(url+game, headers={"accept":"application/xml"}).content

        xml = ET.fromstring(r)
        limit = 6
        start = 0

        found = {}
        idGame = ""

        for g in xml.findall('boardgame'):

            """boardgame"""
            """print(g.tag)"""

            """{'objectid': '13'}"""
            """print(g.attrib)"""

            """13"""
            """print(g.get("objectid"))"""

            """gameName = g.find('name')"""

            """Catane"""
            """print(gameName.text)"""

            """found[start] = { "name": gameName.text, "id": g.get("objectid") }"""
            idGame =  idGame + g.get("objectid")  

            start = start + 1

            if start < limit :
                idGame = idGame +","

            if start >= limit:
                break  

        if idGame != "":

            r2 = get(urlGame+idGame, headers={"accept":"application/xml"}).content
            
            xml2 = ET.fromstring(r2)

            loop = 0


            print("-------------------")
            print(xml2.findall('boardgame'))
            print("-------------------")

            for game in xml2.findall('boardgame'):
                idGame = game.get("objectid")
                name = game.find('name')
                minPlayer = game.find("minplayers")
                maxPlayer = game.find("maxplayers")
                age = game.find("age")
                img = game.find("image")

                found[loop] = {
                    "id" :idGame,
                    "name" : name.text,
                    "minPlayer" : minPlayer.text,
                    "maxPlayer" : maxPlayer.text,
                    "age" : age.text,
                    "img" : img.text
                }

                loop = loop + 1
            
            print("end")

        return found
        