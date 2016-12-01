from flask import render_template, flash, redirect, request
from app import app
from .user_forms import *

from sql.base_sql import SQL, SQLTable

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

    return render_template('search.html',
                            title = 'Find Showings',
                            form=form,
                            table=table)

@app.route('/buy', methods=['GET', 'POST'])
def user_buy():
    attendTable = SQLTable('attend') 
    form = BuyForm()
    
    if form.validate_on_submit():
        attendTable.insert(form.values())
        flash ('You bought tiks')
        redirect('/buy') 

    return render_template('form_renderer.html',
                            title='Buy',
                            form=form)

@app.route('/rate', methods=['GET', 'POST'])
def user_rate():
    form = RateForm()

    if form.validate_on_submit():
        # I should start using python's string.format()
        # forgot it existed (oops)
        command =   ('UPDATE attend '
                    ' SET rating = ' + form.rating.data + 
                    ' WHERE customer_id = \'' + form.customer_id.data + '\''
                    ' AND showing_id = \'' + form.showing_id.data + '\'')
        SQL.command(command)
        flash ('Thanks for rating')
        redirect('/rate') 

    return render_template('form_renderer.html',
                            title='Rate',
                            form=form)


@app.route('/movielog', methods=['GET', 'POST'])
def user_movie():
    form = UserForm()
    table = []

    query = ('SELECT name, rating'
            ' FROM attend NATURAL JOIN showing NATURAL JOIN movie'
            ' WHERE customer_id = \'{}\' ').format(form.customer_id.data)
    table = [('Name', 'Rating')] + SQL.query(query)
    
    if form.validate_on_submit():
        redirect('/movielog') 

    return render_template('search.html',
                            title='Movie Log',
                            table=table,
                            form=form)


@app.route('/userinfo', methods=['GET', 'POST'])
def user_info():
    form = UserForm()
    table = []

    query = ('SELECT * FROM customer'
            ' WHERE customer_id = \'{}\' ').format(form.customer_id.data)
    table =  SQL.query(query)
    
    if form.validate_on_submit():
        redirect('/userinfo') 

    return render_template('search.html',
                            title='User Info',
                            table=table,
                            form=form)

@app.route('/sqlinjection', methods=['GET', 'POST'])
def sql_injection():
    form = UserForm()
    table = []

    query = ('SELECT * FROM attend NATURAL JOIN customer NATURAL JOIN showing NATURAL JOIN movie'
            ' WHERE customer_id = \'{}\' ').format(form.customer_id.data)
    table =  SQL.query(query)
    
    if form.validate_on_submit():
        redirect('/sqlinjection') 

    return render_template('search.html',
                            title='SQL Injection Enabled',
                            table=table,
                            form=form)

@app.route('/sqlinjectionnot', methods=['GET', 'POST'])
def sql_injection_not():
    form = UserForm()
    table = []

    query = ('SELECT * FROM attend NATURAL JOIN customer NATURAL JOIN showing NATURAL JOIN movie'
            ' WHERE customer_id = %(customer_id)s')
    parameters = { 'customer_id' :form.customer_id.data }
    table =  SQL.parameterized_query(query,parameters)
    
    if form.validate_on_submit():
        redirect('/sqlinjectionnot') 

    return render_template('search.html',
                            title='Parameterized Queries, No More Injections',
                            table=table,
                            form=form)
