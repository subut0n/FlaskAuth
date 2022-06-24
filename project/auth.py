import email
from flask import Blueprint, flash, render_template, url_for, redirect, request
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# Login
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


# Sign up
@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # User informations for the db
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if password != confirm_password:
        flash("Password fields do not match")
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first() # If this return a user, then the email already exists in the db

    if user: # If a user is found, redirect back to signup page so user can try again
        flash("User with that email already exists.")
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
 
 # logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))