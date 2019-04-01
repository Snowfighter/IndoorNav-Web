import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses are not cashed
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initiating db object
db = SQLAlchemy(app)


# Table class
class Users(db.Model):
    __tablename__ = 'users'
    tab_id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    tab_username = db.Column('username', db.Text, nullable=False)
    tab_hash = db.Column('hash', db.Text, nullable=False)

    def __init__(self, tab_id, tab_username, tab_hash):
        self.tab_id = tab_id
        self.tab_username = tab_username
        self.tab_hash = tab_hash
