from flask import render_template, flash, redirect, request
from app import app
from .user_forms import *

from sql.base_sql import SQL

@app.route('/search', methods=['GET', 'POST'])
def user_search():
    form = SearchForm() 
    table = []

    # im making a view next time :(
    query = (''
            'SELECT showing_id, name, date, time, available '
            'FROM showing NATURAL JOIN movie NATURAL JOIN genre NATURAL JOIN room NATURAL LEFT JOIN'
                '(SELECT showing_id, \'Yes\' AS available FROM (SELECT showing_id, COUNT(customer_id) as attendees, capacity '
                'FROM showing NATURAL LEFT JOIN attend NATURAL JOIN room GROUP BY showing_id) AS '
                'showing_attendees  WHERE attendees < capacity) AS full_showings '
            'WHERE name LIKE CONCAT(\'%\',\'' + request.form.get('movieTitle') + '\', \'%\') '
            'AND date >= \'' + request.form.get('startDate') + '\' '
            'AND date <= \'' + request.form.get('endDate') + '\' ')
    if request.form.get('genre') != 'ALL_GENRES': 
        query += 'AND genre = \'' + request.form.get('genre') +  '\' '
    if request.form.get('notFull'):
        query += 'AND available LIKE \'Yes\''

    table = [('Showing ID', 'Movie Title', 'Date', 'Time', 'Available')] + SQL.query(query)

    if form.validate_on_submit():
        redirect('/search')
             

    return render_template('form_renderer.html',
                            form=form,
                            table=table)
