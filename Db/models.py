from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(555), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    cover_photo = db.Column(db.String(1000))  

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
