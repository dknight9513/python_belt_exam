from flask import request, redirect, render_template, session, flash
from flask_app.models.painting import Painting

from flask_app import app

@app.route('/dashboard')
def logged_in():
    if 'first_name' in session:
        paintings = Painting.get_all_paintings_and_users()
        data = {'id' : session['user_id']}
        purchased_paintings = Painting.get_all_purchased_paintings(data)
        return render_template('dashboard.html', paintings = paintings, purchased = purchased_paintings)
    flash('You must be logged in to view that page', 'login')
    return redirect('/')

@app.route('/paintings/new')
def new_painting():
    if 'first_name' in session:
        return render_template('newPainting.html')
    flash('You must be logged in to view that page', 'login')
    return redirect('/')

@app.route('/create_painting', methods=['POST'])
def create_painting():
    if 'first_name' in session:
        print(request.form)
        data = {
                'user_id' : session['user_id'],
                'title' : request.form['title'],
                'description' : request.form['description'],
                'price' : request.form['price'],
                'quantity' : request.form['quantity'],
        }
        if(not Painting.validate_painting(data)):
            return redirect('/paintings/new')
        Painting.save(data)
        return redirect('/dashboard')
    flash('You must be logged in to view that page', 'login')
    return redirect('/')

@app.route('/paintings/<int:painting_id>')
def view_painting(painting_id):
    if 'first_name' in session:
        data = { 'id' : painting_id}
        painting = Painting.get_painting_and_user(data)
        if painting:
            return render_template('viewPainting.html', painting = painting)
        else:
            return redirect('/dashboard')
    flash('You must be logged in to view that page', 'login')
    return redirect('/')

@app.route('/paintings/<int:painting_id>/edit')
def editing_painting(painting_id):
    if 'first_name' in session:
        data = { 'id' : painting_id }
        painting = Painting.get_painting(data)
        if(painting):
            if painting.user_id == session['user_id']:
                return render_template('editPainting.html', painting = painting)
            flash('You must be logged in as the creator of that painting to edit it.')
            return redirect('/dashboard')
        flash('That is not a valid painting id')
        return redirect('/dashboard')
    flash('You must be logged in to view that page', 'login')
    return redirect('/')

@app.route('/update/<int:painting_id>', methods=['POST'])
def update_painting(painting_id):
    if 'first_name' in session:
        data1 = { 'id' : painting_id }
        painting = Painting.get_painting(data1)
        if(painting):
            if painting.user_id == session['user_id']:
                data = {
                    'id' : painting_id,
                    'title' : request.form['title'],
                    'description' : request.form['description'],
                    'price' : request.form['price'],
                    'quantity' : request.form['quantity'],
                }
                if(not Painting.validate_painting(data)):
                    return redirect(f"/paintings/{painting_id}/edit")
                Painting.update(data)
                flash('Painting was successfully updated!')
                return redirect('/dashboard')
            flash('You must be logged in as the creator of that painting to edit it.')
            return redirect('/dashboard')
        flash("That is not a valid painting id")
        return redirect('/dashboard')
    flash('You must be logged in to view that page', 'login')
    return redirect('/')

@app.route('/delete/<int:painting_id>')
def delete_painting(painting_id):
    if 'first_name' in session:
        data = { 'id' : painting_id }
        painting = Painting.get_painting(data)
        if(painting):
            if painting.user_id == session['user_id']:
                Painting.delete(data)
                flash("Painting was successfully deleted!")
                return redirect('/dashboard')
            flash('You must be logged in as the creator of that painting to delete it.')
            return redirect('/dashboard')
        flash('That is not a valid painting id')
        return redirect('/dashboard')
    flash('You must be logged in to view that page', 'login')
    return redirect('/')

@app.route('/buy_painting/<int:painting_id>')
def purchase_painting(painting_id):
    if 'first_name' in session:
        data = {'id' : painting_id}
        painting = Painting.get_painting(data)
        if painting:
            if painting.quantity_purchased < painting.quantity:
                new_quantity_purchased = painting.quantity_purchased+1
                data['quantity_purchased'] = new_quantity_purchased
                Painting.buy_painting(data)
                data['user_id'] = session['user_id']
                Painting.new_owner(data)
                flash(f'Thank you very much for the purchase, {session["first_name"]}!')
                return redirect('/dashboard')
            flash('That painting id is completely sold out. Please browse our other pieces.')
            return redirect('/dashboard')
        flash('That is not a valid painting id')
        return redirect('/dashboard')
    flash('You must be logged in to view that page','login')
    return redirect('/')
