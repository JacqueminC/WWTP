from flask import Blueprint, render_template

bpTable = Blueprint("table", __name__, template_folder="templates")

@bpTable.route("/tableForm")
def tableForm():
    return render_template("tableForm.html")

