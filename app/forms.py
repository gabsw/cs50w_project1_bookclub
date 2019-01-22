from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, NumberRange, InputRequired
from app.queries import query_user_username


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_password(self, password):
        username = self["username"]

        user = query_user_username(username=username.data)

        if user is None:
            raise ValidationError('Invalid username or password.')

        if not user.check_password(password.data):
            raise ValidationError('Invalid username or password.')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = query_user_username(username=username.data)

        if user is not None:
            raise ValidationError('Please use a different username.')


class ReviewForm(FlaskForm):
    body = TextAreaField('Critique this book:', validators=[
        DataRequired(), Length(min=1, max=2000)])
    score = IntegerField('Rate this book (1-5):', validators=[
        InputRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search for:', validators=[
        DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Submit')
