from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import secrets


app = Flask(__name__, static_url_path='', static_folder='frontend/secular-lms/build')
app.config['SECRET_KEY'] = secrets.token_hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)

database = SQLAlchemy(app)
import models

from apis import *

if __name__ == "__main__":
    app.run(
        host='localhost',
        port=5000,
        debug=True
    )
