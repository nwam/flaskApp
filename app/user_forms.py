from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from sql.base_sql import SQL

class OrderedForm(FlaskForm):
    def __iter__(self):
        field_order = getattr(self, 'field_order', None)
        if field_order:
            temp_fields = []
            for name in field_order:
                if name == '*':
                    temp_fields.extend([f for f in self._unbound_fields if f[0] not in field_order])
                else:
                    temp_fields.append([f for f in self._unbound_fields if f[0] == name][0])
            self._unbound_fields = temp_fields
        return super(OrderedForm, self).__iter__()

class SearchForm(OrderedForm):
    movieTitle = StringField('Movie Title') 
    startDate = SelectField("Start Date", 
            choices=[(c[0],c[0]) for c in SQL.query(
                'SELECT date FROM showing GROUP BY date ORDER BY date')])
    endDate = SelectField("End Date", 
            choices=[(c[0],c[0]) for c in SQL.query(
                'SELECT date FROM showing GROUP BY date ORDER BY date DESC')])
    genre = SelectField("Genre", 
            choices=[('ALL_GENRES', 'All')] + [(c[0],c[0]) for c in SQL.query(
                'SELECT genre FROM genre GROUP BY genre ORDER BY genre')])
    notFull = BooleanField("Available")
    submit = SubmitField("Search")
