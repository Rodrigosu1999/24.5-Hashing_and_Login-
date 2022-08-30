from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, PasswordField, EmailField
from wtforms.validators import InputRequired, Optional, NumberRange, URL


class AddUserForm(FlaskForm):
    """Form to add new user to db"""
    username = StringField("Username",
                           validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[InputRequired()])
    email = EmailField("Email",
                       validators=[InputRequired()])
    first_name = StringField("First name",
                             validators=[InputRequired()])
    last_name = StringField("Last name",
                            validators=[InputRequired()])


class LoginUserForm(FlaskForm):
    """Form to login user"""
    username = StringField("Username",
                           validators=[InputRequired()])
    password = PasswordField("Password",
                             validators=[InputRequired()])


class AddFeedbackForm(FlaskForm):
    """Form to add new feedback to db"""
    title = StringField("Title",
                        validators=[InputRequired()])
    content = StringField("Content",
                          validators=[InputRequired()])


class UpdateFeedbackForm(FlaskForm):
    """Form to update a feedback"""
    title = StringField("Title",
                        validators=[InputRequired()])
    content = StringField("Content",
                          validators=[InputRequired()])
