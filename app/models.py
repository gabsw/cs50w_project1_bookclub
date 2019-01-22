from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(UserMixin):
    def __init__(self, username, password_hash, user_id=None):
        self.username = username
        self.password_hash = password_hash
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_from_db_record(record):
        # getattr gets the named attribute from the record, if it exists
        # if it doesn't exist, returns a default value, which is set to None below
        # getattr(record, "username", None)
        return User(record.username, record.password_hash, record.id)


class Review:
    def __init__(self, body, score, book_id, user_id, review_id=None):
        self.body = body
        self.score = score
        self.book_id = book_id
        self.user_id = user_id
        self.review_id = review_id

    @staticmethod
    def create_from_db_record(record):
        # this wont work for all queries, as one of them doesnt ask for the ids
        return Review(record.body, record.score, record.book_id, record.user_id, record.id)


class Book:
    def __init__(self, title, author, publication_year, isbn, book_id=None):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.isbn = isbn
        self.book_id = book_id

    @staticmethod
    def create_from_db_record(record):
        return Book(record.title, record.author, record.publication_year, record.isbn, record.id)


class ReviewWithUser:
    def __init__(self, username, body, score):
        self.username = username
        self.body = body
        self.score = score

    @staticmethod
    def create_from_db_record(record):
        return ReviewWithUser(record.username, record.body, record.score)


class UserRating:
    def __init__(self, username, body, score, title, isbn):
        self.username = username
        self.body = body
        self.score = score
        self.title = title
        self.isbn = isbn

    @staticmethod
    def create_from_db_record(record):
        return UserRating(record.username, record.body, record.score, record.title, record.isbn)