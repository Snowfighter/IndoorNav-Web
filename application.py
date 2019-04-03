import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Disable commit tracking
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Path to the database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///./phpLiteAdmin/indoorNav.db'


# Initiating db object
db = SQLAlchemy(app)


# Table class
class User(db.Model):
    __tablename__ = 'users'
    tab_id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    tab_username = db.Column('username', db.Text, unique=True, nullable=False)
    tab_hash = db.Column('hash', db.Text, unique=True, nullable=False)

    def __init__(self, tab_username, tab_hash):
        self.tab_username = tab_username
        self.tab_hash = tab_hash


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


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submiting the form)
    if request.method == "POST":

        # Ensure username was submited
        if not request.form.get("username"):
            return render_template("apology.html")

        # Ensure password was submited
        if not request.form.get("password"):
            return render_template("apology.html")

        # Ensure confirmation was submited
        if not request.form.get("confirmation"):
            return render_template("apology.html")

        # Ensure password matches confirmation
        if not request.form.get("password") == request.form.get("confirmation"):
            return render_template("apology.html")

        # Hash the password
        hash_pas = generate_password_hash(request.form.get("password"))

        # Check if user already exists and add if not
        exists = User.query.filter_by(tab_username=request.form.get("username")).first() is None
        if not exists:
            return render_template("apology.html")
        else:
            new_user = User(tab_username=request.form.get("username"), tab_hash=hash_pas)
            db.session.add(new_user)
            db.session.commit()

            # Get user's id
            current_user = User.query.filter_by(tab_username=request.form.get("username")).first()

            # Log in the user
            session["user_id"] = current_user.tab_id

            # Redirect to homepage
            return redirect("/")

    # User reached route via GET (just getting by link)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any session
    session.clear()

    # User reached route via POST (as by submiting the form)
    if request.method == "POST":

        # Ensure username was submited
        if not request.form.get("username"):
            return render_template("apology.html")

        # Ensure password was submited
        if not request.form.get("password"):
            return render_template("apology.html")

        # Query database for the username
        user = User.query.filter_by(tab_username=request.form.get("username")).first()

        # Ensure the user exits and password is correct
        if user is None or not check_password_hash(user.tab_hash, request.form.get("password")):
            return render_template("apology.html")

        # Remember which user is logged in
        session["user_id"] = user.tab_id

        # Redirect to home page
        return redirect("/")

    # User reached via GET (just getting by link)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log the user out"""

    # Forget any user
    session.clear()

    # Redirect to the home page
    return redirect("/")




