from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user


auth = Blueprint('auth', __name__) # setup auth blueprint for our flask app

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') # has information about request sent to access this root
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')

        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required # Makes sure we cannot access this route unless user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        api_key = request.form.get('apikey')
        user = User.query.filter_by(email = email).first()
        if user:
            flash('User with this email already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be at least four characters.", category='error')
        elif len(firstName) < 2:
            flash("First name must be at least four characters.", category='error')
        elif password1 != password2:
            flash("Passwords do not match.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least seven characters.", category='error')
        else: #add user to database
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='pbkdf2'), 
                            api_key=generate_password_hash(api_key, method='pbkdf2'))

            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))

            
    return render_template("sign_up.html", user=current_user)