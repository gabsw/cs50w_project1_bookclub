from flask import render_template, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash

from app import app
from app.forms import LoginForm, RegistrationForm, ReviewForm, SearchForm
from flask_login import logout_user, current_user, login_user
import app.queries as query
import requests

from config import Config


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        query.query_add_user(username=form.username.data, password_hash=generate_password_hash(form.password.data))
        message = 'Congratulations, you have created a new account!'
        return render_template('success_registration.html', message=message)
    return render_template('registration.html', form=form, title='Registration')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = query.query_user_username(username=form.username.data)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('search'))
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    logout_user()
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('results', search_keyword=form.search.data.strip()))

    return render_template('search.html', form=form, title='Search Engine')


@app.route('/results/<search_keyword>', methods=['GET'])
def results(search_keyword):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    books = query.query_search_books(search_keyword)

    if books is None:
        return render_template("errors.html", message="No such book was found. Try again using different keywords.")

    return render_template('results.html', books=books, title='Search Results')


@app.route('/book/<isbn>', methods=['POST'])
def post_reviews(isbn):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    book = query.query_book(isbn)
    form = ReviewForm()
    if form.validate_on_submit():
        score = int(form.score.data)

        current_user_review = query.query_review_user(current_user.user_id, book.book_id)
        if current_user_review is None:
            query.query_add_review(form.body.data, score, book.book_id, current_user.user_id)
            message = 'Your review has been posted!'
            return render_template("success_review.html", message=message, isbn=isbn, title='Successful Review')
        else:
            return render_template("errors.html", message="You have already reviewed this book.", title='Error')

    return render_template('books.html', form=form, title=book.title, book=book)


@app.route('/book/<isbn>', methods=['GET'])
def get_book_reviews(isbn):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    book = query.query_book(isbn)
    if book is None:
        return render_template("errors.html", message="A book with this ISBN doesn't exist in our database.",
                               title='Error')

    reviews = query.query_all_reviews(book.book_id)
    number_reviews = query.count_reviews(book.book_id)

    if len(reviews) == 0:
        avg_score = "This book hasn't been rated yet by our users."
    else:
        avg_score = query.calculate_average_score(book.book_id)

    user_has_review = False
    for review in reviews:
        if review.username == current_user.username:
            user_has_review = True
            break

    form = ReviewForm() if not user_has_review else None

    # Goodreads API
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": Config.GOODREADS_KEY, "isbns": isbn})

    if res.status_code != 200:
        count_goodreads_reviews = "Not Available"
        avg_goodreads_score = "Not Available"
    else:
        data = res.json()
        book_list = data['books']
        book_stats = book_list[0]
        count_goodreads_reviews = book_stats["work_ratings_count"]
        avg_goodreads_score = book_stats["average_rating"]

    return render_template('books.html', book=book, reviews=reviews, number_reviews=number_reviews, avg_score=avg_score,
                           user_has_review=user_has_review, form=form, count_goodreads_reviews=count_goodreads_reviews,
                           avg_goodreads_score=avg_goodreads_score, title=book.title)


@app.route('/user_review/<user_id>/<isbn>', methods=['GET'])
def get_user_book_review(user_id, isbn):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    book = query.query_book(isbn)
    review = query.query_review_user(user_id, book.book_id)

    if review is None:
        return render_template("errors.html", message="This user hasn't reviewed this book.",
                               title='Error')
    return render_template('user_review.html', book=book, review=review, title='User Review')


@app.route("/api/<isbn>")
def books_api(isbn):
    book = query.query_book(isbn)
    if book is None:
        return jsonify({"error": "Invalid book isbn."}), 404

    book_id = book.book_id
    number_reviews = query.count_reviews(book_id)

    reviews = query.query_all_reviews(book_id)
    if reviews is None:
        avg_score = "This book hasn't been rated yet by our users."
    else:
        avg_score = query.calculate_average_score(book_id)

    return jsonify(
        {
            "title": book.title,
            "author": book.author,
            "year": book.publication_year,
            "isbn": book.isbn,
            "review_count": number_reviews,
            "average_score": avg_score
        })


@app.route('/user/<username>')
def user(username):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    user = query.query_user_username(username)
    if user is None:
        return render_template("errors.html", message="This user doesn't exist in our database.",
                               title='Error')

    user_reviews = query.query_user_ratings(username)
    avg_score_user = query.calculate_average_score_per_user(user.user_id)
    if avg_score_user is None:
        avg_score_user = "N/A"

    number_user_reviews = query.count_reviews_per_user(user.user_id)

    return render_template('user_profile.html', user=user, user_reviews=user_reviews,
                           number_user_reviews=number_user_reviews, avg_score_user=avg_score_user,
                           title='User Profile')