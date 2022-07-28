from datetime import datetime
from app import db

# Models (classes) that represent a database table. Each instance of the class is a row.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    files = db.relationship('File', backref='owner', lazy='dynamic')

    def __init__(self, email, password_hash, first_name, last_name):
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User {} - email: {} - Name: {} {}>'.format(self.id, self.email, self.first_name, self.last_name)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120))
    uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    file_type = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, file_name, uploaded, file_type, user_id):
        self.file_name = file_name
        self.uploaded = uploaded,
        self.file_type = file_type
        self.user_id = user_id

    def __repr__(self):
        return f'File id: {self.id} - file_name: {self.file_name} - uploaded: {self.uploaded} - file_type: {self.file_type} - user_id: {self.user_id}'