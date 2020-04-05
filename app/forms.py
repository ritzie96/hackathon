from flask import flash
from wtforms import Form, StringField, SubmitField, IntegerField, SelectField, SelectMultipleField, MultipleFileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from app.models import Employee, User
import re

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    municipality = StringField('Municipality')
    register = SubmitField('Register')

    def validate_username(self, field):
        e_ids = [cv.username for cv in User.query.all()]
        if field.data in e_ids:
            flash(f'Username already exists', 'danger')
            raise ValidationError('Please try to login')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    login = SubmitField('Login')

    def validate_username(self, field):
        e_ids = [cv.username for cv in User.query.all()]
        if field.data not in e_ids:
            flash(f'User does not exist. Please Register.', 'danger')
            raise ValidationError('Please try to register')


class SearchForm(FlaskForm):
    municipality = SelectField('Municipality', choices = [('', ''), ('Österåker', 'Österåker'), ('Nacka', 'Nacka'), ('Nykvarn', 'Nykvarn'), ('Tyresö', 'Tyresö'), ('Huddinge', 'Huddinge'), ('Södertälje', 'Södertälje'), ('Vallentuna', 'Vallentuna'), ('Nynäshamn', 'Nynäshamn'), ('Solna', 'Solna'), ('Vaxholm', 'Vaxholm'), ('Botkyrka', 'Botkyrka'), ('Upplands-Bro', 'Upplands-Bro'), ('Järfälla', 'Järfälla'), ('Upplands Väsby', 'Upplands Väsby'), ('Sollentuna', 'Sollentuna'), ('Haninge', 'Haninge'), ('Ekerö', 'Ekerö'), ('Danderyd', 'Danderyd'), ('Stockholm', 'Stockholm'), ('Sundbyberg', 'Sundbyberg'), ('Norrtälje', 'Norrtälje'), ('Värmdö', 'Värmdö'), ('Täby', 'Täby'), ('Sigtuna', 'Sigtuna'), ('Lidingö', 'Lidingö'), ('Salem', 'Salem')])
    keywords = StringField('Keywords')
    search = SubmitField('Search')
