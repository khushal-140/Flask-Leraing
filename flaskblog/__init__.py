from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail  import Mail
from flaskblog.config import Config




db=SQLAlchemy() # This initializes the SQLAlchemy object with the Flask application, allowing us to interact with the database using SQLAlchemy's ORM (Object-Relational Mapping) features.
bcrypt = Bcrypt()
login_manager = LoginManager() # This initializes the LoginManager object with the Flask application, which is used to manage user authentication and session management in the application.
login_manager.login_view = 'users.login' # This sets the login view for the LoginManager. It specifies that if a user tries to access a protected route without being authenticated, they will be redirected to the 'login' view (which is defined in the routes.py file).
login_manager.login_message_category = 'info' # This sets the category for the flash message that


mail=Mail()

#from flaskblog import routes # This imports the routes module from the flaskblog package, which contains the route definitions for the application. This is done at the end to avoid circular imports, as the routes module will need to import the app object defined in this __init__.py file.




def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app