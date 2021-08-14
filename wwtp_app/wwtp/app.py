#print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from datetime import datetime
from flask import Flask, render_template, session, make_response
import logging
from flask_pymongo import PyMongo
from table.table import bpTable
from home.home import bpHome
from joueur.joueur import bpJoueur
from evaluation.evaluation import bpEvaluation
from auth.auth import bpAuth
from flask_bootstrap import Bootstrap

app = Flask(__name__)


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
    """session["user"] = {
        "idJoueur": "60c86295cbbfd4f430693f17",
        "dateDeNaissance" : datetime(1988, 10, 8, 0,0,0),        
        "note" : 0,
        "nom" : "Random Guy",
        "pseudo" : "Cédric"
        }"""

    """session.pop("user", None)
    session["isLogged"] = False"""
    app.logger.debug("I'm a DEBUG message")
    app.logger.info("I'm an INFO message")
    app.logger.warning("I'm a WARNING message")
    app.logger.error("I'm a ERROR message")
    app.logger.critical("I'm a CRITICAL message")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

    gunicorn_logger = logging.getLogger('/var/log/gunicorn/gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)