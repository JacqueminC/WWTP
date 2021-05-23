#print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from flask import Flask, render_template
from flask_pymongo import PyMongo
from wwtp.table.table import bpTable
from wwtp.home.home import bpHome
from flask_bootstrap import Bootstrap


app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey"
app.config["MONGO_URI"] = "mongodb://localhost:27017/wwtp"

Bootstrap(app)

mongodb_client = PyMongo(app)
db = mongodb_client.db

app.register_blueprint(bpTable, url_prefix="/table")
app.register_blueprint(bpHome, ulr_prefix="/home")

@app.route("/")
@app.route("/index")
def index():
    #testDb = mongo.db.cedric.find()
    #testDb = mdb.cedric.find_one_or_404({"name": "Cédric"})
    #db.cedric.insert_one({"name":"frodon", "last":"Sacquet", "job":"destroy one ring"})

    return render_template("index.html")

if __name__ == "wwtp.app":
    app.run(debug=True)

