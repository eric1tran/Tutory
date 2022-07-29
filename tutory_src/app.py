from flask import Flask, render_template, request, flash, redirect, url_for
from user_forms import LoginForm, RegistrationForm
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, logout_user

from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from models import User, File

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
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # POST with valid data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        if password != confirm_password:
            flash('Passwords do not match')
        else:
            user = User(email, password, first_name, last_name)
            file = File('File001', datetime.now(), '.jpg', '1')

    return render_template('register.html', form=form)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profile')
def profile():
    return "My Profile Settings"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))