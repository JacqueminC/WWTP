from flask import Blueprint, render_template

bpHome = Blueprint("home", __name__, static_folder="static", template_folder="templates")

@bpHome.route("/home")
@bpHome.route("/")
def home():
    return "Welcome Home!!!"