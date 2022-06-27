from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField #input fields
from wtforms.validators import InputRequired, Email, EqualTo #validators = email ensures email structure is followed, EqualTo compares two password inputs
from ..models import User
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address', validators = [InputRequired(),Email()])
    username = StringField('Enter your username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired(), EqualTo('password_confirm', message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators = [InputRequired()])
    submit = SubmitField('Sign Up')

    #custom validators
    def validate_email(self, data_field): #takes in the data field and checks in the database
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('The email already exists')
        
    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address', validators = [InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me') #confirms the user wants to be logged out after the session
    submit = SubmitField('Sign in')
