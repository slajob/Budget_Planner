from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ExpensesForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    amount = FloatField('amount', validators=[DataRequired()])
    monthno = IntegerField('monthno', default = datetime.utcnow().strftime("%m"))
    exorin = SelectField(u'Expense or Income', choices=[('Expense', 'Expense'), ('Income', 'Income')])

    add = SubmitField('Add record')

class MonthChooseForm(FlaskForm):
    choosemonth = IntegerField('Filter by month', default=datetime.utcnow().strftime("%m"))
    show = SubmitField('Show')