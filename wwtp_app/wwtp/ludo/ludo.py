from flask import Blueprint, render_template,session, request, redirect, url_for, flash

bpLudo = Blueprint("ludo", __name__, template_folder="templates")

@bpLudo.route("/", methods=["GET", "POST"])
def myLudo():
    pass