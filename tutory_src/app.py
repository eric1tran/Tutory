from flask import Flask, render_template, request, flash, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'index'

from models import User, File
from user_forms import LoginForm, RegistrationForm

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'File': File}


@app.route('/', methods=['GET', 'POST'])
def index():
    # If logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        # Search for user
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))

        # login_user will register the user as logged in (i.e. sets current_user to user)
        login_user(user)
        next_page = request.args.get('next')
        # if next_page is not set or url is a relative URL (doesn't have a hostname, only a path), go to home page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # POST with valid data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(email, password, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/profile')
@login_required
def profile():
    return "My Profile Settings"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))