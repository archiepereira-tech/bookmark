import csv
import datetime
import pytz
import requests
import urllib
import uuid
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def configure():
   load_dotenv()

# Built using the help of Google Gemini (AI):
# Using Google Books API
def lookup(title):
  """Look for book title"""

  # API key
  key = os.getenv("api_key")

  # Build the Google Books service object
  service = build("books", "v1", developerKey=key)

  # Define the search query
  query = {}
  query["q"] = title

  # Make the search request
  try:
    results = service.volumes().list(q=query["q"]).execute()
    books = results.get("items", [])

    # Return info about the first book
    if books:
      book = books[0]
      volume_info = book["volumeInfo"]
      return {"title": volume_info.get("title"), "authors": volume_info.get("authors", []), "publishedDate": volume_info.get("publishedDate"), "description": volume_info.get("description"), "pagecount": volume_info.get("pageCount"), "thumbnail": volume_info.get("imageLinks"), "infolink": volume_info.get("infoLink")}
    else:
      return None

  except Exception as e:
    print(f"Error: {e}")
    return None
