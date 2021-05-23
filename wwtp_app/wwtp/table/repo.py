print("REPO")
print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

from .. import app
print("data.size => {0}".format(app.size))
print("------------------------{0}".format(app.app.config["MONGO_URI"]))




class RepoTable:
    def FindAll():   
        return "flask.jsonify(result)"

