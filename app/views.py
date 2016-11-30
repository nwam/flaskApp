from flask import render_template, flash, redirect, request
from app import app
from .forms import *

from app.sql.base_sql import SQLTable

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'nwam'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for "%s"' %
            (form.username.data))
        return redirect('/index')
    return render_template('login.html',
                            title='Sign In',
                            form=form)

## backend views ## 

@app.route('/admin/movie', methods=['GET', 'POST'])
def admin_movie():
    movieTable = SQLTable('movie', ' ORDER BY name ASC') 
    table = movieTable.query_all()
    print(table)
    addForm = MovieAddForm()
    remForm = MovieRemForm()
    modForm = MovieModForm()

    if addForm.validate_on_submit() and "addSubmit" in request.form:
        flash('Successfully added ' + addForm.name.data + ' to database.')
        movieTable.insert(addForm.values())
        return redirect('/admin/movie')

    if remForm.validate_on_submit() and "remSubmit" in request.form:
        movieTable.remove(remForm.pk())
        return redirect('/admin/movie')

    if modForm.validate_on_submit() and "modSubmit" in request.form:
        movieTable.modify(remForm.mod_value(), remForm.values())
        return redirect('/admin/movie')

    return render_template('admin_movie.html',
                            title='Movies',
                            table=table,
                            addForm=addForm,
                            remForm=remForm,
                            modForm=modForm)

