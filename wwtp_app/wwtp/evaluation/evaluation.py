from flask import Blueprint, render_template,session, request, redirect, url_for, flash
from werkzeug.utils import redirect
"""
from wwtp.table.model import Table
from .model import Joueur
"""


bpEvaluation = Blueprint("joueur", __name__, template_folder="templates")