from flask import Blueprint, app, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, BooleanField, FormField, FieldList
from wtforms.fields.html5 import IntegerRangeField
#from flask_bootstrap import Bootstrap

bpTable = Blueprint("table", __name__, template_folder="templates")

class JeuxListeForm(FlaskForm):
    nom = StringField("Nom du jeu : ")
    version = StringField("Version du jeu")

class CreationTableForm(FlaskForm):
    #hote = StringField('hote')
    jeuxLibre = BooleanField(' Jeux libre ?')
    nbPlace = IntegerField('Nombre de place disponnible')
    jeux = StringField('Jeux')
    date = DateTimeField('Date')
    ville = StringField('Ville')
    ageMin = BooleanField('Définir un âge minimum ?')
    age = IntegerField(' Age minimum ?')
    regle = BooleanField(' Connaissance des règles requises ?')
    noteMin = BooleanField(' Note minimum ?')
    note = IntegerRangeField('Note')

@bpTable.route("/tableForm", methods=["GET", "POST"])
def creationTable():
    form = CreationTableForm()

    if form.validate_on_submit():
        return "Form envoyé! {} and {}".format(form.jeuxLibre.data, form.date.data)

    return render_template("tableForm.html", form=form)


"""
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50))
    phone = db.relationship(lambda: PhoneNumber)
    
class PhoneNumber(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    phonetype = db.Column(db.String(10))
    number = db.Column(db.String(20))
    ext = db.Column(db.String(10))

class PhoneNumberForm(Form):
    phonetype = SelectField(gettext("Type"), choices=[(c, c) for c in ['Mobile', 'Home', 'Work', 'Fax', 'Other']])
    number = TelField(gettext("Number"), validators=[Required()])
    ext = TextField(gettext("Notes"), validators=[Optional()])
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(PhoneNumberForm, self).__init__(csrf_enabled=False, *args, **kwargs)

class ModelFieldList(FieldList):
    def __init__(self, *args, **kwargs):         
        self.model = kwargs.pop("model", None)
        super(ModelFieldList, self).__init__(*args, **kwargs)
        if not self.model:
            raise ValueError("ModelFieldList requires model to be set")

    def populate_obj(self, obj, name):
        while len(getattr(obj, name)) < len(self.entries):
            newModel = self.model()
            db.session.add(newModel)
            getattr(obj, name).append(newModel)
        while len(getattr(obj, name)) > len(self.entries):
            db.session.delete(getattr(obj, name).pop())
        super(ModelFieldList, self).populate_obj(obj, name)

class UserForm(Form):
    username = TextField(gettext("Username"), validators=[Required()])
    phone = ModelFieldList(FormField(PhoneNumberForm), model=PhoneNumber)
    submit = SubmitField(gettext("Submit"))

    @app.route("/")
def index()
    user = User.query.first()
    form = UserForm(obj = user)
    form.phone.min_entries=3
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
    return render_template("page.html", form = form)
    
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.add(User(username="Frank"))
    db.session.commit()
    app.run(debug=True)

"""

"""
<body>
        {{ form.username.label }}: {{ form.username }}
        <div data-toggle="fieldset" id="phone-fieldset">
            {{ form.phone.label }} <button type="button" data-toggle="fieldset-add-row" data-target="#phone-fieldset">+</button>
            <table>
                <tr>
                    <th>Type</th>
                    <th>Number</th>
                    <th>Extension</th>
                    <th></th>
                </tr>
                {% for phone in form.phone %}
                <tr data-toggle="fieldset-entry">
                    <td>{{ phone.phonetype }}</td>
                    <td>{{ phone.number }}</td>
                    <td>{{ phone.ext }}</td>
                    <td><button type="button" data-toggle="fieldset-remove-row" id="phone-{{loop.index0}}-remove">-</button></td>
                </tr>
                {% endfor %}
            </table>
        </div>
        {{ form.submit }}
        <script src="{{ url_for("static", filename="js/jquery-1.10.2.min.js") }}"></script>
        <script src="{{ url_for("static", filename="js/page.js") }}"></script>
    </body>
"""

"""
$(function() {
    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);
            
            //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function() {
            var target = $($(this).data("target"))
            console.log(target);
            var oldrow = target.find("div[data-toggle=fieldset-entry]:last");
            var row = oldrow.clone(true, true);
            console.log(row.find(":input")[0]);
            var elem_id = row.find(":input")[0].id;
            var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
            row.attr('data-id', elem_num);
            row.find(":input").each(function() {
                console.log(this);
                var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
                $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
            });
            oldrow.after(row);
        }); //End add new entry

                //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
            if($this.find("div[data-toggle=fieldset-entry]").length > 1) {
                var thisRow = $(this).closest("div[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
    });
});
"""
