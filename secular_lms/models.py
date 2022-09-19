from dataclasses import dataclass
from flask_login import UserMixin
from main import database, login_manager
from sqlalchemy.sql import func


@dataclass
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    first_name = database.Column(database.String(50), nullable=False)
    last_name = database.Column(database.String(50), nullable=True)
    email_id = database.Column(database.String(20), unique=True, nullable=False)
    phone_number = database.Column(database.Integer, nullable=False)
    address = database.Column(database.String(500), nullable=False)
    username = database.Column(database.String(20), unique=True, nullable=False)
    password = database.Column(database.String(100), nullable=False)

    def as_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_id': self.email_id,
            'phone_number': self.phone_number
        }


@dataclass
class Book(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    book_title = database.Column(database.String(50), nullable=False)
    isbn = database.Column(database.String(50), nullable=False)
    book_author = database.Column(database.String(50), nullable=False)
    in_stock = database.Column(database.Integer, nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'book_title': self.book_title,
            'isbn': self.isbn,
            'book_author': self.book_author,
            'in_stock': self.in_stock
        }


@dataclass
class Rented(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    book_id = database.Column(database.Integer, database.ForeignKey('book.id', ondelete='CASCADE'))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id', ondelete='SET NULL'))
    book_rented_on = database.Column(database.DateTime(), server_default=func.now(), nullable=False)
    book_returned_on = database.Column(database.DateTime(), onupdate=func.now(), nullable=True)

    def as_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'book_rented_on': self.book_rented_on,
            'book_returned_on': self.book_returned_on
        }


# Login configuration
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(
        id=user_id).first()

database.create_all()
