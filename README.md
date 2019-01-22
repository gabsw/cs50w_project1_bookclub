# BOOKCLUB

The goal of this project is to create a web application that works as a search engine and aggregator of reviews for books.

## Design
The implementation has followed the contents taught in the [**CS50W course**](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/), through lectures 0 to 4. My main objective was to get acquainted with the Flask framework.

The structure of the backend was broken down according to the following logic:

* Routes: contains the logic to handle requests to the application.
* Models: contains all the classes that have been created to obtain objects that store information from the database (User, Book, Review, ReviewWithUser).
* Forms: contains all the forms that were used to obtain information. These were implemented as WTForms.
* Queries: contains all the queries written in SQL that were used throughout the project, to provide easier consultation.

The frontend components can be found in the ````templates```` folder, which contains eleven HTML files.

The PostgreSQL database was implemented through SQLAlchemy, which is  a Python SQL toolkit. The queries used for the creation of the table can be consulted by checking the files ```import.py```

The visual styling was implemented through the Flask-Bootstrap plugin and ````style.css````.

## Key Features

* User Logins
* User Profile
* Search Engine
* Posting Reviews
* Bookclub's API
* Requests to Goodreads' API
