from flask import Blueprint, flash, render_template, request, redirect, url_for
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, login_manager

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email direction or password, try again.', category='error')
        else:
            flash('Incorrect email direction or password, try again.', category='error')
    
    return render_template("auth/login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signUp():
    email = ""
    first_name = ""
    password1 = ""
    password2 = ""
    
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif not is_valid_email(email):
            flash('Incorrect email direction.', category='error')
        elif first_name == "":
            flash('First Name empty.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif not is_valid_password(password1):
            flash('Password must be at least 8 characters long and contain both letters and numbers.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            
            return redirect(url_for('views.home'))
            
    return render_template("auth/signup.html", user=current_user, email=email, first_name=first_name)

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True