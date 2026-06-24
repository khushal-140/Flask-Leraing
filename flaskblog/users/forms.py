from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), 
                            Length(min=2, max=20)])
    email= StringField('Email' , validators=[DataRequired(),Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password=StringField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    
    submit=SubmitField('Sign Up')   
    def validate_username(self,username):
        
        user=User.query.filter_by(username=username.data).first()# This line queries the database to check if there is already a user with the same username as the one entered in the registration form. It uses SQLAlchemy's query interface to filter the User table by the username field and retrieves the first result. If a user with that username exists, it will return a User object; otherwise, it will return None.
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')# If a user with the same username is found in the database, this line raises a ValidationError with a message indicating that the username is already taken. This will prevent the form from being submitted and will display the error message to the user, prompting them to choose a different username.

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()# This line queries the database to check if there is already a user with the same email as the one entered in the registration form. It uses SQLAlchemy's query interface to filter the User table by the email field and retrieves the first result. If a user with that email exists, it will return a User object; otherwise, it will return None.
        if user: 
            raise ValidationError('That email is taken. Please choose a different one.')# If a user with the same email is found in the database, this line raises a ValidationError with a message indicating that the email is already taken. This will prevent the form from being submitted and will display the error message to the user, prompting them to choose a different email address.


class loginForm(FlaskForm): 
    email= StringField('Email' , validators=[DataRequired(),Email()])
    remember=BooleanField('Remember Me')#For cooked to remember the user for some time longer than the session logout
    password= PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Log In')
    
    
    
    
class UpdateAccountForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), 
                            Length(min=2, max=20)])
    email= StringField('Email' , validators=[DataRequired(),Email()])
    picture=FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])# This line defines a file upload field for updating the user's profile picture. The FileAllowed validator restricts the allowed file types to JPG and PNG images, ensuring that users can only upload valid image files for their profile picture.
    
    
    submit=SubmitField('Update') 
      
    def validate_username(self,username):
        if username.data != current_user.username: # This line checks if the username entered in the update account form is different from the current user's username. This is important because if the user is not changing their username, we don't want to raise a validation error for a username that already exists (which would be their own username).
            user=User.query.filter_by(username=username.data).first()# This line queries the database to check if there is already a user with the same username as the one entered in the registration form. It uses SQLAlchemy's query interface to filter the User table by the username field and retrieves the first result. If a user with that username exists, it will return a User object; otherwise, it will return None.
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')# If a user with the same username is found in the database, this line raises a ValidationError with a message indicating that the username is already taken. This will prevent the form from being submitted and will display the error message to the user, prompting them to choose a different username.


    def validate_email(self,email):
        if email.data != current_user.email: # This line checks if the email entered in the update account form is different from the current user's email. This is important because if the user is not changing their email, we don't want to raise a validation error for an email that already exists (which would be their own email).
            user=User.query.filter_by(email=email.data).first()# This line queries the database to check if there is already a user with the same email as the one entered in the registration form. It uses SQLAlchemy's query interface to filter the User table by the email field and retrieves the first result. If a user with that email exists, it will return a User object; otherwise, it will return None.
            if user: 
                raise ValidationError('That email is taken. Please choose a different one.')# If a user with the same email is found in the database, this line raises a ValidationError with a message indicating that the email is already taken. This will prevent the form from being submitted and will display the error message to the user, prompting them to choose a different email address.
    
class RequestResetForm(FlaskForm):
    email= StringField('Email' , validators=[DataRequired(),Email()])
    submit=SubmitField('Request Password Reset ')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email . you must have to register first ')
 
class ResetPasswordForm(FlaskForm):
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password=StringField('Confirm Password', validators=[DataRequired(),EqualTo('password')])    
    
    submit=SubmitField('Reset Password')