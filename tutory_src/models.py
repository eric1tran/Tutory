from app import db

# Models (classes) that represent a database table. Each instance of the class is a row.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User {} - email: {} - Name: {} {}>'.format(self.id, self.email, self.first_name, self.last_name)