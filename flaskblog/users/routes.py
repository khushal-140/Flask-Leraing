from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm,  UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, loginForm)
from flaskblog.users.utils import save_picture, send_reset_email


users= Blueprint('users',__name__)



@users.route('/register',methods=['GET','POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')# This line takes the password entered by the user in the registration form, hashes it using bcrypt, and then decodes it to a UTF-8 string. This is done to securely store the password in the database without saving it in plain text.
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)# This line creates a new User object with the username, email, and hashed password obtained from the registration form. The User class is defined in the models.py file and represents a user in the database. The username and email are taken directly from the form data, while the password is stored as a hashed version for security reasons.
        db.session.add(user) # This line adds the newly created User object to the current database session. It prepares the user to be inserted into the database when the session is committed.
        db.session.commit() # This line commits the current database session, which means that all changes
               
       
        flash('your account has been created! You can now log in.', 'success')# success is the category of the flash message, which can be used to style the message differently in the template (e.g., green for success, red for error).
        return redirect(url_for('users.login'))# After successfully creating an account, the user is redirected to the home page. The url_for function is used to generate the URL for the home route.
    return render_template('register.html', title='Register', form=form)



@users.route('/login',methods=['GET','POST'])
def login():    
    if(current_user.is_authenticated):
            return redirect(url_for('main.home'))
    form = loginForm()
   
    if form.validate_on_submit():
        
        user=User.query.filter_by(email=form.email.data).first()# This line queries the database to find a user with the email address entered in the login form. It uses SQLAlchemy's query interface to filter the User table by the email field and retrieves the first result. If a user with that email exists, it will return a User object; otherwise, it will return None.
        if user and bcrypt.check_password_hash(user.password, form.password.data):# This line checks if a user was found with the provided email and if the password entered in the login form matches the hashed password stored in the database for that user. The bcrypt.check_password_hash function takes the hashed password from the database and the plain text password from the form, hashes the plain text password, and compares it to the stored hash. If both conditions are true (user exists and password is correct), it will return True; otherwise, it will return False. 
            login_user(user, remember=form.remember.data) # This line logs in the user using Flask-Login's login_user function. It takes the user object that was retrieved from the database and a boolean value indicating whether to remember the user for future sessions (based on the "Remember Me" checkbox in the login form). If remember is True, Flask-Login will set a long-term cookie to keep the user logged in even after closing the browser.
            next_page=request.args.get('next') # This line retrieves the value of the "next" parameter from the query string of the request. The "next" parameter is typically used to store the URL that the user was trying to access before being redirected to the login page. If there is a "next" parameter, it means that the user was trying to access a protected route and was redirected to the login page.
            return redirect(next_page) if next_page else redirect(url_for('main.home'))# After successfully logging in, the user is redirected to the home page. The url_for function is used to generate the URL for the home route.  
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():    
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():# This line checks if the form has been submitted and if all the validators for the form fields have passed. If this condition is true, it means that the user has submitted the form with valid data, and we can proceed to update their account information.
        
        if form.picture.data: # This line checks if the user has uploaded a new profile picture in the account update form. If this condition is true, it means that the user has selected a new image file to upload as their profile picture, and we can proceed to save the new image and update the user's profile picture in the database.
            picture_file=save_picture(form.picture.data) # This line calls a function named save_picture, passing the uploaded picture file from the form as an argument. The save_picture function is responsible for saving the uploaded image file to the server and returning the filename of the saved image. The returned filename is then stored in the picture_file variable, which can be used to update the user's profile picture in the database.
            current_user.image=picture_file # This line updates the current user's profile picture in the database by setting the image attribute of the current_user object to the filename of the newly uploaded picture (stored in picture_file). This change will be saved to the database when we commit the session later on.
        
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit() # This line commits the current database session, which means that all changes made to the current_user object (such as updating the username and email) will be saved to the database.
        flash('Your account has been updated!', 'success')# This line flashes a success message to the user indicating that their account has been updated. The 'success' category can be used to style the message differently in the template (e.g., green for success).
        return redirect(url_for('users.account'))# After updating the account information, the user is redirected   
    elif request.method == 'GET': # This line checks if the request method is GET, which means that the user is accessing the account page to view their current account information. If this condition is true, we populate the form fields with the current user's existing username and email so that they can see their current information when they access the account page.
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image) # This line generates the URL for the user's profile image. It uses the url_for function to create a URL for the static folder, specifically for the profile_pics subfolder, and appends the filename of the user's image (which is stored in the current_user.image_file attribute). This allows the template to display the user's profile picture correctly.
    return render_template('account.html', title='Account', image_file= image_file, form=form)   


@users.route("/user/<string:username>")
def user_posts(username):
    
    page=request.args.get('page',1,type=int) # This line retrieves the value of the "page" parameter from the query string of the request. If the "page" parameter is not present in the query string, it defaults to 1. The type=int argument ensures that the retrieved value is converted to an integer. This is used for pagination, allowing users to navigate through different pages of posts. 
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=3)   # This line queries the database to retrieve all the posts stored in the Post table. It uses SQLAlchemy's query interface to access the Post model and calls the all() method to get a list of all Post objects from the database. The retrieved posts are then stored in the posts variable, which can be passed to the template for rendering.
    return render_template('user_posts.html',posts=posts,user=user)

@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))    
    form=RequestResetForm()
    if form.validate_on_submit():
        user =User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send with instruction to reset your password.','info')
        return redirect(url_for('users.login'))
        
    return render_template('reset_request.html',title="Reset Password",form=form)



@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if(current_user.is_authenticated):
        return redirect(url_for('main.home')) 
    user = User.verify_reset_token(token)
    if user is None:
        flash("Then is invaild or expired token ",'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        
            
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')# This line takes the password entered by the user in the registration form, hashes it using bcrypt, and then decodes it to a UTF-8 string. This is done to securely store the password in the database without saving it in plain text.
        user.password= hashed_password
        db.session.commit() # This line commits the current database session, which means that all changes
                   
           
        flash('your password has been updated ! You can now log in.', 'success')# success is the category of the flash message, which can be used to style the message differently in the template (e.g., green for success, red for error).
        return redirect(url_for('users.login'))    
    return render_template('reset_token.html',title="Reset Password",form=form)