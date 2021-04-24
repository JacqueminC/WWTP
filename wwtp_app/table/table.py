from flask import Blueprint, render_template

bpTable = Blueprint("table", __name__, static_folder="static", template_folder="templates")

@bpTable.route("/tableForm")
def tableForm():
    return render_template("tableForm.html")