from flask import Blueprint, render_template, session
from werkzeug.utils import redirect

bpHome = Blueprint("home", __name__, template_folder="templates")

@bpHome.route("/home", methods=["GET", "POST"])
def home():
    if session.get("isLogged"):
        return render_template("home.html")
    else:
        return redirect("/")