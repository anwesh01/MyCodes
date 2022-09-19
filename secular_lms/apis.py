import datetime
from main import app, send_from_directory, database
import flask
from flask_login import login_user, logout_user, current_user, login_required
import json
import models
from sqlalchemy.sql import column


@app.route("/index", methods=['GET'])
def load_index():
    return send_from_directory(app.static_folder, 'index.html')


# change password
@app.route('/signup', methods=['POST'])
def signup():
    info = json.loads(flask.request.data)

    # validation not performed

    user = models.User()

    user.first_name = info.get('first_name')
    user.last_name = info.get('last_name',None)
    user.email_id = info.get('email_id')
    user.phone_number = info.get('phone_number')
    user.address = info.get('address')
    user.username = info.get('username')
    user.password = info.get('password')

    database.session.merge(user)
    database.session.commit()

    return flask.jsonify({
        "status": 200
    }), 200


# change password
@app.route('/login', methods=['POST'])
def login():
    info = json.loads(flask.request.data)
    username = info.get('username', None)
    password = info.get('password', None)

    if not username or not password:
        return flask.jsonify({
            "status": 401,
            "reason": "Username or Password Error"
        }), 401

    # encode the password
    user = models.User.query.filter_by(
        username=username,
        password=password
    ).first()

    if user:
        login_user(user)
        return flask.jsonify({
            "status": 200,
            "data": user.as_dict()
        }), 200

    return flask.jsonify({
        "status": 401,
        "reason": "Username or Password Error"
    }), 401


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return flask.jsonify(**{
        'status': 200,
        'data': {'message': 'logout success'}
    })


@app.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {
            "status": 200,
            "data": current_user.to_json()
        }
    else:
        resp = {
            "status": 401,
            "data": {"message": "user not login"}
        }
    return flask.jsonify(**resp)


@app.route('/books', methods=['GET'])
@login_required
def get_books():
    books_cursor = models.Book.query.all()
    response = {
        "status": 200,
        "data": []
    }
    for book in books_cursor:
        response['data'].append(book.as_dict())

    return flask.jsonify(response)


@app.route('/rented-currently', methods=['GET'])
@login_required
def get_books_rented_currently():
    user = current_user._get_current_object()

    rented_cursor = models.Rented.query.filter_by(
        user_id=user.id
    ).filter(
        column('book_returned_on').is_(None)
    ).all()

    response = {
        "status": 200,
        "data": []
    }

    for rented in rented_cursor:
        book = models.Book.query.filter_by(
            id=rented.book_id
        ).first()

        rented_book= book.as_dict()
        rented_book.update(rented.as_dict())
        rented_book['ids'] = {}
        rented_book['ids']['book_id'] = book.id
        rented_book['ids']['rented_id'] = rented.id
        response['data'].append(rented_book)

    return flask.jsonify(response)


@app.route('/rented-history', methods=['GET'])
@login_required
def get_books_rented_history():
    user = current_user._get_current_object()

    rented_cursor = models.Rented.query.filter_by(
        user_id=user.id
    ).filter(
        column('book_returned_on').is_not(None)
    ).all()

    response = {
        "status": 200,
        "data": []
    }

    for rented in rented_cursor:
        book = models.Book.query.filter_by(
            id=rented.book_id
        ).first()

        rented_book=book.as_dict()
        rented_book.update(rented.as_dict())
        response['data'].append(rented_book)

    return flask.jsonify(response)


@app.route('/books/return', methods=['GET'])
@login_required
def return_book():
    user = current_user._get_current_object()

    info = flask.request.args
    book_id = info.get('book_id', None)
    rented_id = info.get('rented_id', None)

    if not book_id or not rented_id:
        return flask.jsonify({
            "status": 400,
            "reason": "Book Id or Rented Id cannot be Null"
        }), 400

    rented_book = models.Rented.query.filter_by(
        id=rented_id
    ).first()

    rented_book.book_returned_on = datetime.datetime.now()

    # book is now available
    rented_book = models.Book.query.filter_by(
        id=book_id
    ).first()
    rented_book.in_stock += 1

    database.session.commit()

    response = {
        "status": 200
    }

    return flask.jsonify(response)


@app.route('/books/rent', methods=['GET'])
@login_required
def rent_book():
    user = current_user._get_current_object()

    info = flask.request.args
    book_id = info.get('book_id', None)

    if not book_id:
        return flask.jsonify({
            "status": 400,
            "reason": "Book Id cannot be Null"
        }), 400

    # unique combination of book_id,user_id
    book_to_rent = models.Book.query.filter_by(
        id = book_id
    ).first()

    if book_to_rent.in_stock  == 0:
        return flask.jsonify({
            "status": 400,
            "reason": "No Stock Available"
        }), 400

    book_to_rent.in_stock -= 1

    rented = models.Rented()
    rented.book_id = book_to_rent.id
    rented.user_id = user.id
    rented.book_rented_on = datetime.datetime.now()

    database.session.merge(rented)
    database.session.commit()

    response = {
        "status": 200
    }

    return flask.jsonify(response)


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    return "hi"
