#print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from flask import Flask, render_template, make_response, Blueprint, request, jsonify
import logging
from table.table import bpTable
from home.home import bpHome
from joueur.joueur import bpJoueur
from evaluation.evaluation import bpEvaluation
from auth.auth import bpAuth
from ludo.ludo import bpLudo
from flask_bootstrap import Bootstrap

bp = Blueprint('main', __name__)

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/wwtp"

import pwa

Bootstrap(app)

app.register_blueprint(bp)
app.register_blueprint(pwa.bp)
app.register_blueprint(bpTable, url_prefix="/table")
app.register_blueprint(bpHome, ulr_prefix="/home")
app.register_blueprint(bpJoueur, url_prefix="/joueur")
app.register_blueprint(bpEvaluation, url_prefix="/evaluation")
app.register_blueprint(bpAuth, url_prefix="/auth")
app.register_blueprint(bpLudo, url_prefix="/myludo")

@app.route("/")
@app.route("/index")
def index():

    resp = make_response(render_template("index.html"))
    resp.set_cookie('idUser', '', expires=0)    

    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)    
    gunicorn_logger = logging.getLogger('gunicorn.error')

