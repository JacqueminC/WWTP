from flask import Blueprint, render_template

bpTable = Blueprint("table", __name__, static_folder="static", template_folder="templates")

@bpTable.route("/table")
@bpTable.route("/")
def tableForm():
    return "table form"