from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from werkzeug.utils import redirect
from .model import Evaluation


bpEvaluation = Blueprint("evaluation", __name__, template_folder="templates")

@bpEvaluation.route("/evaluerJoueur", methods=["GET", "POST"])
def notePlayer():
    note = request.args.get('note')
    idPlayer = request.args.get('idPlayer')
    idTable = request.args.get('idTable')

    user = session["user"]
    idJoueur = user["idJoueur"]

    Evaluation.createEvaluation(idTable, idPlayer, idJoueur, int(note), "dice")

    return redirect(url_for('joueur.evaluatePlayer'))


