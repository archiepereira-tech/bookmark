import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, configure

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookmark.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """ Show bookmarks for current book """
    # Retrieve current title
    current_title = db.execute("SELECT current_title FROM users WHERE users.id = ?", session["user_id"])
    current_title = current_title[0]["current_title"]

    # Retrieve current page
    current_page = db.execute("SELECT current_page FROM users WHERE users.id = ?", session["user_id"])
    current_page = current_page[0]["current_page"]
    if not current_page:
        current_page = 0

    # Get table of bookmarks from current book
    current_bookmarks_db = db.execute("SELECT page, datetime FROM bookmarks WHERE bookmarks.id = ? AND title = ? ORDER BY datetime DESC", session["user_id"], current_title)

    # Decide whether alert is needed
    has_read_today = db.execute("SELECT has_read_today FROM users WHERE users.id = ?", session["user_id"])
    has_read_today = has_read_today[0]["has_read_today"]

    return render_template("index.html", current_bookmarks=current_bookmarks_db, current_title=current_title, current_page=current_page, alert=has_read_today)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add bookmark of book"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Save book title
        book_title = request.form.get("title")
        # Return apology if no title is provided
        if not book_title:
            return apology("missing title", 400)

        # Save page number
        page_number = request.form.get("pages")
        # Return apology if no number of pages is provided
        if not page_number:
            return apology("missing page number", 400)
        # Return apology if the input is not numerical
        if not page_number.isdigit():
            return apology("page number must be a number", 400)
        # Convert string to int
        page_number = int(float(page_number))
        # Return apology if the number of pages is not a positive number
        if page_number <= 0:
            return apology("page number must be greater than or equal to 1", 400)

        # Insert into database
        db.execute("INSERT INTO bookmarks (id, title, page) VALUES (?, ?, ?)", session["user_id"], book_title, page_number)
        has_read = True
        db.execute("UPDATE users SET current_title = ?, current_page = ?, has_read_today = ? WHERE users.id = ?", book_title, page_number, has_read, session["user_id"])

        # Redirect to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")


@app.route("/history")
@login_required
def history():
    """Show history of bookmarks"""

    history_db = db.execute("SELECT title, page, datetime FROM bookmarks WHERE bookmarks.id = ? ORDER BY datetime DESC", session["user_id"])

    return render_template("history.html", history=history_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure password and confirmation matches
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("passwords must match", 400)

        # Ensure username does not already exist
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) >= 1:
            return apology("username already exists", 400)

        # Save user into database
        PASSWORDHASH = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), PASSWORDHASH)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove bookmarks of book"""

    # Get titles for dropdown
    saved_titles = db.execute("SELECT title FROM bookmarks WHERE bookmarks.id = ? GROUP BY title", session["user_id"])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # If user has not provided title
        if not request.form.get("title"):
            return apology("missing title", 400)
        # If user has not provided page number
        if not request.form.get("pages"):
            return apology("missing page number", 400)
        # If number of pages is not a positive number
        elif int(request.form.get("pages")) <= 0:
            return apology("shares must be positive", 400)
        # Get number of pages for validation
        saved_pages = db.execute("SELECT page FROM bookmarks WHERE bookmarks.id = ? AND title = ? AND page = ?", session["user_id"], request.form.get("title"), request.form.get("pages"))
        if not saved_pages:
            return apology("page number must be bookmarked for selected title", 400)

        # Update database
        db.execute("DELETE FROM bookmarks WHERE bookmarks.id = ? AND title = ? AND page = ?", session["user_id"], request.form.get("title"), request.form.get("pages"))

        # Update current page
        new_current_page = db.execute("SELECT page FROM bookmarks WHERE bookmarks.id = ? AND title = ? ORDER BY datetime DESC", session["user_id"], request.form.get("title"))
        if not new_current_page:
            new_current_page = 0
        else:
            new_current_page = new_current_page[0]["page"]
        db.execute("UPDATE users SET current_page = ? WHERE users.id = ?", new_current_page, session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("remove.html", titles=saved_titles)


@app.route("/bookinfo")
@login_required
def bookinfo():
    """Get info about user's current title from Google Books API"""
    # Configure API key
    configure()

    # Retrieve current title
    current_title = db.execute("SELECT current_title FROM users WHERE users.id = ?", session["user_id"])
    current_title = current_title[0]["current_title"]

    # Check if book title is available in Google Books
    gb_title = lookup(current_title)

    return render_template("bookinfo.html", info=gb_title)
