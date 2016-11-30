from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])

class MovieForm():
    id = StringField('ID') 
    name = StringField('Name')
    year = StringField('Year')
    current_id = StringField('Current ID')

    def pk(self):
        return self.id.data

    def mod_value(self):
        return self.current_id.data

    def values(self):
        return [self.id.data, self.name.data, self.year.data]

class MovieAddForm(FlaskForm, MovieForm):
    addSubmit = SubmitField("Add")
class MovieRemForm(FlaskForm, MovieForm):
    remSubmit = SubmitField("Remove")
class MovieModForm(FlaskForm, MovieForm):
    modSubmit = SubmitField("Modify")
