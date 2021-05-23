from flask import Blueprint, render_template

bpHome = Blueprint("home", __name__, template_folder="templates")

@bpHome.route("/home")
def home():
    return render_template("home.html")