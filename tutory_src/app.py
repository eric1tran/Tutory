from flask import Flask, render_template, request, flash
from user_forms import LoginForm, RegistrationForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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
        print(f'{email=}, {password=}, {confirm_password=}')
        if password != confirm_password:
            errors = 'Passwords do not match'
            flash('Passwords do not match')
    return render_template('register.html', form=form)


@app.route('/home')
def home():
    return "Home Page"