from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])

# MOVIE # 
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

# ROOM # 
class RoomForm():
    id = StringField('ID') 
    capacity = StringField('Capacity')
    current_id = StringField('Current ID')

    def pk(self):
        return self.id.data

    def mod_value(self):
        return self.current_id.data

    def values(self):
        return [self.id.data, self.capacity.data]

class RoomAddForm(FlaskForm, RoomForm):
    addSubmit = SubmitField("Add")
class RoomRemForm(FlaskForm, RoomForm):
    remSubmit = SubmitField("Remove")
class RoomModForm(FlaskForm, RoomForm):
    modSubmit = SubmitField("Modify")

# CUSTOMER # 
class CustomerForm():
    id = StringField('ID') 
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    sex = StringField('Sex')
    email = StringField('Email')
    current_id = StringField('Current ID')

    def pk(self):
        return self.id.data

    def mod_value(self):
        return self.current_id.data

    def values(self):
        return [self.id.data, self.first_name.data, self.last_name.data, self.sex.data, self.email.data]

class CustomerAddForm(FlaskForm, CustomerForm):
    addSubmit = SubmitField("Add")
class CustomerRemForm(FlaskForm, CustomerForm):
    remSubmit = SubmitField("Remove")
class CustomerModForm(FlaskForm, CustomerForm):
    modSubmit = SubmitField("Modify")

# SHOWING # 
class ShowingForm():
    id = StringField('ID') 
    movie_id = StringField('Movie ID')
    room_id= StringField('Room ID')
    date = StringField('Date')
    time = StringField('Time')
    current_id = StringField('Current ID')

    def pk(self):
        return self.id.data

    def mod_value(self):
        return self.current_id.data

    def values(self):
        return [self.id.data, self.movie_id.data, self.room_id.data, self.date.data, self.time.data]

class ShowingAddForm(FlaskForm, ShowingForm):
    addSubmit = SubmitField("Add")
class ShowingRemForm(FlaskForm, ShowingForm):
    remSubmit = SubmitField("Remove")
class ShowingModForm(FlaskForm, ShowingForm):
    modSubmit = SubmitField("Modify")


# GENRE #
class GenreForm():
    movie_id = StringField('Movie ID')
    genre = StringField('Genre') 

    def values(self):
        return [ self.movie_id.data, self.genre.data]

class GenreAddForm(FlaskForm, GenreForm):
    addSubmit = SubmitField("Add")
class GenreRemForm(FlaskForm, GenreForm):
    remSubmit = SubmitField("Remove")

