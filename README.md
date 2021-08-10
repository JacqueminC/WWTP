# WWTP
Projet TFE

installer un environement virtuel (env)
python3 -m venv venv
lancer l'environement virtuel
.\env\Scripts\active (env)

installer les dépendances avec pip en étant sous env
pip install flask
pip install pytest
pip install flask_pymongo
pip install flask-wtf
pip install flask-bootstrap
pip install flask_admin
pip install python-dateutil
pip install Flask-Mail
pip install flask-login

pip list
python .\main.py


Quand j'ai voulu installer sur l'environement
- Flask-PyMongo
- pytest

J'ai du le faire en local pour que cela puisse également fonctionner

J'ai eu un soucis au niveau des imports, impossible d'avoir accès à la variable app dans app.py, il a fallut modifier la structure avec qu'il concidére app.py dans un package
### Ceci permet de voir le nom du fichier, le nom et le package
print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

pour la lancer l'app j'utilisais ceci:
if __name__ == "__main__":
    app.run(debug=True)

mais avec la modfication je dois faire ceci:
if __name__ == "wwtp.app":
    app.run(debug=True)

mon app.py est bien dans un package mais de ce fait n'est plus comme __main__

nginx start
gunicorn app:app
sudo mongod --fork --logpath /var/log/mongodb/mongodb.log