from cmath import log
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User
from . import auth
from .. import db
from ..email import mail_message

@auth.route('/register', methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to Pitches", "email/welcome_user", user.email, user=user)

        return redirect(url_for('auth.login')) #the user can now login to the the application so we redirect them to the login route
        title = "New Account"
    return render_template('auth/register.html', registration_form = form)

@auth.route('/login',methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data) #this is a flask login extension to record the user as logged for that session, it takes user object and remembers form data, if true it sets a long time cookie in your browser
            return redirect(request.args.get('next') or url_for('main.index'))  

        flash('invalid username or password')
    
    title = "watchlist login"
    return render_template('auth/login.html', login_form = login_form, title = title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))