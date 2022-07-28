from flask import Flask, render_template, request, flash
from user_forms import LoginForm, RegistrationForm
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User

@app.route('/', methods=['GET', 'POST'])
def index():
    # If logged in, redirect to home

    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    errors = None

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
            print(repr(user))

    return render_template('register.html', form=form)


@app.route('/home')
def home():
    return "Home Page"