from flask import Flask, render_template
from flask_pymongo import PyMongo
from table.table import bpTable
from home.home import bpHome
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

if __name__ == "__main__":
    app.run(debug=True)

