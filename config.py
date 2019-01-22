import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-text'
    DATABASE_URL = os.environ.get('DATABASE_URL') or None  # will fail when connecting to the db
    GOODREADS_KEY = os.environ.get('GOODREADS_KEY') or None
    GOODREADS_SECRET = os.environ.get('GOODREADS_SECRET') or None
