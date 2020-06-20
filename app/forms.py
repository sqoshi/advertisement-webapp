from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, IntegerField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.validators import ValidationError, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    """ Collecting user data to login """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class DeleteAnnForm(FlaskForm):
    """ Taking id of ann to be deleted """
    id = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class AnnouncementForm(FlaskForm):
    """ Collecting data to create Announce """
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[Length(min=0, max=140)])
    phone = StringField('Phone Number')
    submit = SubmitField(' Add')


class EditAnnForm(FlaskForm):
    """ Collecting data to edit Announce """
    id = IntegerField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[Length(min=0, max=140)])
    phone = StringField('Phone Number')
    submit = SubmitField(' Edit')


class RegistrationForm(FlaskForm):
    """ Collecting data to register user """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Unique user
        :param username:
        :return:
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """
        Email need to be in form xxx@xxx.xx
        :param email:
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    """ Collecting data to edit user info """
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
