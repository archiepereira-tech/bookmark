# Bookmark
#### Video Demo:  [Click Here to View on YouTube](https://youtu.be/gd4MExlKa9E)
#### Description: Bookmark is a powerful digital bookmarking tool for physical books that allows users to add and remove bookmarks, view their bookmarks and reading history, and learn more about their current book using the Google Books API. Below are descriptions of the different files used in this Flask-based application and the process of their creation.
## app.py
This Python file is where the main code is located, and it uses Flask to connect all the routes and render all the HTML templates together to form the application. Many valuable libraries, such as the CS50 library and the Flask library, are imported at the top of the file and are necessary to the proper function of Bookmark. Another Python file, helpers.py, is also imported as it contains many important functions, such as lookup(), which is used to retrieve information about a title in the Google Books API, and apology(), which is used to send the user an apology if an error occurs. This file, app.py, uses an SQLite3 database titled bookmarks.db, which stores the user's personal data and bookmarks.

In **index()**, the application retrieves the user's current title from their row in the users table in bookmarks.db, so that it can be displayed on the homepage. The current title was initially going to be generated in the index() function based on the latest bookmark, but it became an addition to the users table in bookmarks.db so that the current title could easily be accessed anywhere in the program. The user's current page is also retrieved from the users table in bookmarks.db, and it was also initially decided to be generated in the index() function; however, it became an addition to the users table as well. Then, a table of all the bookmarks for the current title and user is retrieved to display on the homepage, and index() finally checks if the Boolean has_read_today in the users table in bookmarks_db is true or false so that it can decide whether to send the reading reminder to the home screen or not. This alert was a last-minute decision, as there initially weren't going to be any alerts, but it made sense to persuade the user to use the application and read more often through a reading reminder. The notification was initially going to be used if the user did not read for 3-5 days, but the daily, frequent reminder was implemented as it promoted further reading. The HTML file for the homepage, index.html, is rendered, and all the retrieved information is sent through placeholders to be used in the HTML file through Jinja.

In **add()**, the application allows the user to add a bookmark by rendering the HTML template, add.html, via the GET route, allowing users to fill out a form with the title of their book and the page number of the bookmark they want to place. Once submitted, the program validates the values, returning error codes through the apology() function from helpers.py if the values are not correct, updating bookmarks.db by changing the current title and whether the user has read or not in the users table, and inserting the new bookmark into the bookmark table through the POST route. This function then redirects the user to the homepage, where they can view their bookmarks.

In **history()**, history.html is rendered, and the bookmarks table from bookmarks.db is sent through a placeholder to be displayed as a table with the help of Jinja for the user to view all their bookmarks for all their books.

In **login()**, any user id is forgotten, and the GET route renders the login.html template, which gives users a form to fill out and, once submitted, the POST route validates the username and password (saved as a hash for security) by querying through the users table in bookmarks.db and finally updating the current session to the user's session.

In **logout()**, the session is cleared, and the user is redirected to the login page.

In **register()**, the session is cleared, and the GET route renders register.html, which provides the users with a form to fill out and, once submitted, validates the username, password, and confirmation. Then, the new username and password (which has been hashed for security) is saved into the users table in bookmarks.db, and the user is redirected to the login page, where they can log in with their new credentials.

In **remove()**, the user's titles are retrieved from the bookmarks table in bookmarks.db to give users options on which title they would like to remove a bookmark from via the form provided when remove.html is rendered through the GET route. The requested title and page number are then fully validated in the POST route, and the bookmarks table in bookmarks.db is updated by deleting the selected row. The user's page numbers for the title wanting to be removed are also retrieved from the database for validation before the database is updated. Finally, the new current page is found using an SQLite3 query and updated in the users table in the database, and the user is redirected to the home page.

In **bookinfo()**, the Google Books API key is configured using a function in helpers.py, configure(), and the current title the user is reading is retrieved from the users table in bookmarks.db so that it could be used as an argument in lookup(), which searches the Google Books API for information about the book, as defined in helpers.py as well. This function then renders bookinfo.html and sends the lookup() results through a placeholder to be used with Jinja in the HTML file, allowing the user to view information about the book they are currently reading.

## helpers.py
This Python file contains functions that are used to assist the main file, app.py, and includes functions like lookup(), apology(), configure(), and more. At the top of the file, there are many necessary libraries such as os, googleapiclient.discovery, dotenv, and Flask that are used to develop the functions, hide the Google Books API key, and help configure the API as well.

In **apology()**, the error code and error message are received, reformatted, and apology.html is rendered to display the error.

In **login_required()**, the application makes sure that any restricted page for registered users only is hidden from those without credentials.

In **configure()**, the load_dotenv() function is called from the dotenv library, so the .env file containing the API key can be loaded for usage in lookup(). This function is called before lookup() in bookinfo(), which is defined in the app.py file.

In **lookup()**, the user's current book title is queried into the Google Books API, and relevant information is found to be displayed to the user. This function was developed with the guidance of Google Gemini, an advanced generative AI chatbot developed by Google, which provides the Google Books API. Since this was my first experience with implementing an API, Gemini helped explain how to build the Google Books service object, define the search query, and how to format the search request. The API key is safely stored in a .env file, and with the help of configure(), the key is accessed in the program using os.getenv from the os library. Dictionaries with the user's current book information are then sent back to app.py to be displayed to the user.

## /templates
This folder contains all the HTML files used in this application, including layout.html, which every template is built off of. Jinja is used for if conditions in instances such as whether to display the reading reminder to the current user or not and to iterate over variables using for loops. Variables that are displayed in the HTML files are also displayed using Jinja. Bootstrap is used for many elements throughout the application, such as the accordion, cards, navbar, and more. In addition, the images used for the cards on the home page are licensed using Unsplash's free license. There were many design choices that shifted throughout the development process, such as whether to include cards or whether to add a heading to each page. In the end, the choices made were to create an easy-to-use experience for the user and to be visually pleasing and functional.

## /static
This folder contains all the images used throughout the application, including the logo, which was created digitally by myself, and the favicon. Also, the CSS file (styles.css) is stored in /static and is used throughout the whole operation.
