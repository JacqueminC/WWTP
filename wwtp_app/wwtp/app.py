#print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from datetime import datetime
from flask import Flask, render_template, session, make_response
from flask_login import LoginManager 
import flask
from flask_pymongo import PyMongo
from wwtp.table.table import bpTable
from wwtp.home.home import bpHome
from wwtp.joueur.joueur import bpJoueur
from wwtp.evaluation.evaluation import bpEvaluation
from wwtp.auth.auth import bpAuth
from flask_bootstrap import Bootstrap

app = Flask(__name__)
login_manager = LoginManager()


app.config['SECRET_KEY'] = "secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/wwtp"

Bootstrap(app)

#mongodb_client = PyMongo(app)
#db = mongodb_client.db

app.register_blueprint(bpTable, url_prefix="/table")
app.register_blueprint(bpHome, ulr_prefix="/home")
app.register_blueprint(bpJoueur, url_prefix="/joueur")
app.register_blueprint(bpEvaluation, url_prefix="/evaluation")
app.register_blueprint(bpAuth, url_prefix="/auth")

@app.route("/")
@app.route("/index")
def index():

    resp = make_response(render_template("index.html"))
    """resp.set_cookie('idUser', 'the username')"""
    resp.set_cookie('idUser', '', expires=0)
    """session.pop("idUser", None)"""
    session["user"] = {
        "idJoueur": "60c86295cbbfd4f430693f17",
        "dateDeNaissance" : datetime(1988, 10, 8, 0,0,0),        
        "note" : 0,
        "nom" : "Random Guy",
        "pseudo" : "Cédric"
        }

    return render_template("index.html")

if __name__ == "wwtp.app":
    app.run(debug=True)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)