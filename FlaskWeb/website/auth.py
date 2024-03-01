from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route("/login", methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        # if user exist check for password correction
        if user:
            if check_password_hash(user.password, password): # check that stored password hash matches the given password (line 42)
                flash("Logged in succesfully", category='success')
                login_user(user, remember = True) # remembering the fact that user logged in until he clears the data from the session
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')

        else:
            flash("Email doesnt exist", category='error')

    return render_template("login.html",user = current_user)

@auth.route("/logout")
@login_required # if user not Logged - cant access this page
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods =['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email already exist", category='error')
        if len(email) < 4:
            flash('Email greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('Email greater than 1 characters', category='error')
        elif len(password1) < 3:
            flash('Too short password', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='scrypt'))
            db.session.add(new_user) 
            db.session.commit()
            login_user(user, remember = True)
            flash('Account registerd', category='success')
            return redirect(url_for('views.home'))
            pass
        
    return render_template("signUp.html", user = current_user)
