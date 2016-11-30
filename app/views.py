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


@app.route('/admin/room', methods=['GET', 'POST'])
def admin_room():
    roomTable = SQLTable('room', ' ORDER BY room_id ASC') 
    table = roomTable.query_all()
    print(table)
    addForm = RoomAddForm()
    remForm = RoomRemForm()
    modForm = RoomModForm()

    if addForm.validate_on_submit() and "addSubmit" in request.form:
        flash('Successfully added ' + "a new room" + ' to database.')
        roomTable.insert(addForm.values())
        return redirect('/admin/room')

    if remForm.validate_on_submit() and "remSubmit" in request.form:
        roomTable.remove(remForm.pk())
        return redirect('/admin/room')

    if modForm.validate_on_submit() and "modSubmit" in request.form:
        roomTable.modify(remForm.mod_value(), remForm.values())
        return redirect('/admin/room')

    return render_template('admin_room.html',
                            title='Rooms',
                            table=table,
                            addForm=addForm,
                            remForm=remForm,
                            modForm=modForm)

