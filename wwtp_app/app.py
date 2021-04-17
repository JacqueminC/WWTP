from flask import Flask, render_template
from table.table import bpTable
from home.home import bpHome

app = Flask(__name__)
app.register_blueprint(bpTable, url_prefix="/table")
app.register_blueprint(bpHome, ulr_prefix="/home")

@app.route("/")
def index():
    return "index"

if __name__ == "__main__":
    app.run(debug=True)