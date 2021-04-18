from flask import Blueprint, render_template

bpTable = Blueprint("table", __name__, static_folder="static", template_folder="templates")

@bpTable.route("/table")
def tableForm():
    return "Table form!!!"