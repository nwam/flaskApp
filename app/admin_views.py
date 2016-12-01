from flask import render_template, flash, redirect, request
from app import app
from .admin_forms import *

from app.sql.base_sql import SQLTable

## backend views ## 
@app.route('/admin')
def admin_landing():
    return render_template('admin_landing.html')

@app.route('/admin/movie', methods=['GET', 'POST'])
def admin_movie():
    movieTable = SQLTable('movie', ' ORDER BY name ASC') 
    table = movieTable.query_all()
    addForm = MovieAddForm()
    remForm = MovieRemForm()
    modForm = MovieModForm()

    if addForm.validate_on_submit() and "addSubmit" in request.form:
        movieTable.insert(addForm.values())
        flash('Successfully added ' + addForm.name.data + ' to database.')
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
    addForm = RoomAddForm()
    remForm = RoomRemForm()
    modForm = RoomModForm()

    if addForm.validate_on_submit() and "addSubmit" in request.form:
        roomTable.insert(addForm.values())
        flash('Successfully added ' + "a new room" + ' to database.')
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


@app.route('/admin/customer', methods=['GET', 'POST'])
def admin_customer():
    customerTable = SQLTable('customer', ' ORDER BY last_name ASC') 
    table = customerTable.query_all()
    addForm = CustomerAddForm()
    remForm = CustomerRemForm()
    modForm = CustomerModForm()

    if addForm.validate_on_submit() and "addSubmit" in request.form:
        customerTable.insert(addForm.values())
        flash('Successfully added ' + "a new customer" + ' to database.')
        return redirect('/admin/customer')

    if remForm.validate_on_submit() and "remSubmit" in request.form:
        customerTable.remove(remForm.pk())
        return redirect('/admin/customer')

    if modForm.validate_on_submit() and "modSubmit" in request.form:
        customerTable.modify(remForm.mod_value(), remForm.values())
        return redirect('/admin/customer')

    return render_template('admin_customer.html',
                            title='Customers',
                            table=table,
                            addForm=addForm,
                            remForm=remForm,
                            modForm=modForm)


@app.route('/admin/attend')
def admin_attend():
    query = '''
            SELECT customer_id, showing_id, rating, price first_name, last_name, date, time, name, movie_id  
            FROM attend NATURAL JOIN customer NATURAL JOIN showing NATURAL JOIN movie
            ORDER BY rating DESC
            '''
    table = SQLTable.query(query)

    return render_template('table_view.html',
                            title='Attends',
                            table=table)


@app.route('/admin/showing', methods=['GET', 'POST'])
def admin_showing():
    showingTable = SQLTable('showing', ' ORDER BY date, time') 
    table = showingTable.query_all()
    addForm = ShowingAddForm()
    remForm = ShowingRemForm()
    modForm = ShowingModForm()

    if addForm.validate_on_submit() and "addSubmit" in request.form:
        showingTable.insert(addForm.values())
        flash('Successfully added ' + "a new showing" + ' to database.')
        return redirect('/admin/showing')

    if remForm.validate_on_submit() and "remSubmit" in request.form:
        showingTable.remove(remForm.pk())
        return redirect('/admin/showing')

    if modForm.validate_on_submit() and "modSubmit" in request.form:
        showingTable.modify(remForm.mod_value(), remForm.values())
        return redirect('/admin/showing')

    return render_template('admin_showing.html',
                            title='Showings',
                            table=table,
                            addForm=addForm,
                            remForm=remForm,
                            modForm=modForm)


@app.route('/admin/genre', methods=['GET', 'POST'])
def admin_genre():
    genreTable = SQLTable('genre') 
    query = 'SELECT genre, name FROM genre NATURAL JOIN movie ORDER BY genre ASC, name ASC'
    table = genreTable.query(query)
    addForm = GenreAddForm()
    remForm = GenreRemForm()

    if addForm.validate_on_submit() and "addSubmit" in request.form:
        genreTable.insert(addForm.values())
        flash('Successfully added ' + "a new genre" + ' to database.')
        return redirect('/admin/genre')

    if remForm.validate_on_submit() and "remSubmit" in request.form:
        removeCommand = 'DELETE FROM genre WHERE genre.genre = \'' + remForm.genre.data + '\' AND genre.movie_id = \'' + remForm.movie_id.data + '\''
        genreTable.command(removeCommand)
        return redirect('/admin/genre')
        
    return render_template('admin_genre.html',
                            title='Genres',
                            table=table,
                            addForm=addForm,
                            remForm=remForm)
