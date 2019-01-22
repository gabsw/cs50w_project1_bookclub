from flask import Flask
from config import Config
from flask_login import LoginManager
from .queries import query_user_id
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)


@login.user_loader
def load_user(user_id):
    return query_user_id(user_id)


from app import routes
