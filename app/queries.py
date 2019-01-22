from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.models import User, Book, ReviewWithUser, UserRating
from config import Config

if Config.DATABASE_URL is None:
    raise Exception('DATABASE_URL environment variable is not set')

engine = create_engine(Config.DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


def query_all_users():
    record_list = db.execute(
        """
        SELECT * FROM users;
        """
    ).fetchall()
    return [User.create_from_db_record(record) for record in record_list]


def query_user_id(user_id):
    user_record = db.execute(
        """
        SELECT * FROM users WHERE id=:id
        """, {"id": user_id}
    ).fetchone()
    return User.create_from_db_record(user_record)


def query_user_username(username):
    user_record = db.execute(
        """
        SELECT * FROM users WHERE username=:username
        """, {"username": username}
    ).fetchone()

    if user_record is None:
        return None
    return User.create_from_db_record(user_record)


def query_add_user(username, password_hash):
    db.execute(
        """
        INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)
        """,
        {"username": username, "password_hash": password_hash}
    )
    db.commit()


def query_add_review(body, score, book_id, user_id):
    db.execute(
        """
        INSERT INTO reviews (body, score, book_id, user_id) VALUES (:body, :score, :book_id, :user_id)
        """,
        {"body": body, "score": score, "book_id": book_id, "user_id": user_id}
    )

    db.commit()


def query_book(isbn):
    book_record = db.execute(
        """
        SELECT * FROM books WHERE isbn=:isbn
        """,
        {"isbn": isbn}
    ).fetchone()
    if book_record is None:
        return None
    return Book.create_from_db_record(book_record)


def query_search_books(search_keyword: str):
    record_list = db.execute(
        """
        SELECT * FROM books 
        WHERE upper(title) like :search_keyword or isbn like :search_keyword or
         upper(author) like :search_keyword;
        """,
        {"search_keyword": '%' + search_keyword.upper() + '%'}
    ).fetchall()

    if len(record_list) == 0:
        return None
    return [Book.create_from_db_record(record) for record in record_list]


def query_review_user(user_id, book_id):
    record = db.execute(
        """
        SELECT users.username, reviews.body, reviews.score FROM
        users INNER JOIN reviews ON users.id = reviews.user_id
        WHERE reviews.book_id = :book_id AND users.id = :user_id;
        """,
        {"book_id": book_id, "user_id": user_id}
    ).fetchone()

    if record is None:
        return None
    return ReviewWithUser.create_from_db_record(record)


def query_all_reviews(book_id):
    record_list = db.execute(
        """
        SELECT users.username, reviews.body, reviews.score, reviews.user_id FROM
        users INNER JOIN reviews ON users.id = reviews.user_id
        WHERE reviews.book_id = :book_id;
        """,
        {"book_id": book_id}
    ).fetchall()

    return [ReviewWithUser.create_from_db_record(record) for record in record_list]


def count_reviews(book_id):
    number_reviews = db.execute(
        """
        SELECT COUNT(*) as c FROM reviews
        WHERE reviews.book_id = :book_id
        """,
        {"book_id": book_id}
    ).fetchone()

    return number_reviews.c


def calculate_average_score(book_id):
    result = db.execute(
        """
        SELECT ROUND( AVG( score ), 2) as avg_score FROM reviews 
        WHERE reviews.book_id = :book_id
        """,
        {"book_id": book_id}
    ).fetchone()

    if result.avg_score is None:
        return None

    return float(result.avg_score)


def query_user_ratings(username):
    record_list = db.execute(
        """
        SELECT users.username, reviews.body, reviews.score, books.title, books.isbn FROM
        users INNER JOIN reviews ON users.id = reviews.user_id INNER JOIN books ON reviews.book_id = books.id
        WHERE users.username = :username;
        """,
        {"username": username}
    ).fetchall()

    if record_list is None:
        return None
    return [UserRating.create_from_db_record(record) for record in record_list]


def count_reviews_per_user(user_id):
    number_reviews = db.execute(
        """
        SELECT COUNT(*) as per_user FROM reviews
        WHERE reviews.user_id = :user_id
        """,
        {"user_id": user_id}
    ).fetchone()

    return number_reviews.per_user


def calculate_average_score_per_user(user_id):
    result = db.execute(
        """
        SELECT ROUND( AVG( score ), 2) as avg_score FROM reviews 
        WHERE reviews.user_id = :user_id
        """,
        {"user_id": user_id}
    ).fetchone()

    if result.avg_score is None:
        return None

    return float(result.avg_score)