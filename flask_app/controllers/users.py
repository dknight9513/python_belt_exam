from flask import request, redirect, render_template, session, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def main_page():
    return render_template('mainPage.html')

@app.route('/register', methods = ['POST'])
def register():
    data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : request.form['password'],
            'confirm_password' : request.form['confirm_password']
    }
    if(not User.validate_registration(data)):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(data['password'])
        data['password'] = pw_hash
        User.save(data)
        user = User.get_user_info(data['email'])
        session['first_name'] = user.first_name
        session['user_id'] = user.id
        session['email'] = user.email
        return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }
    user = User.get_user_info(data['email'])
    if(not user):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    elif(not bcrypt.check_password_hash(user.password, data['password'])):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    else:
        session['first_name'] = user.first_name
        session['user_id'] = user.id
        session['email'] = user.email
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
