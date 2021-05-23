import flask


from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/wwtp"

mongodb_client = PyMongo(app)
db = mongodb_client.db


class RepoTable:
    def FindAll():   
        print(app.config["MONGO_URI"])     
        return "flask.jsonify(result)"

