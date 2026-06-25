from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer 

@login_manager.user_loader # This is a decorator provided by Flask-Login that registers the decorated function as the user loader callback. Flask-Login will call this function to load a user from the database based on their user ID when needed (e.g., during login or when accessing protected routes).
def load_user(user_id):
    return User.query.get(int(user_id))# This function is used by Flask-Login to load a user from the database based on their user ID. The @login_manager.user_loader decorator registers this function as the user loader callback, which Flask-Login will call to retrieve a user object when needed (e.g., during login or when accessing protected routes). The function takes a user_id as an argument, converts it to an integer, and queries the User model to find and return the corresponding user object from the database. If no user is found with that ID, it will return None.

class User(db.Model, UserMixin):    
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image=db.Column(db.String(20), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True) # This line defines a relationship between the User model and the Post model. It indicates that a user can have multiple posts. The backref parameter creates a virtual column in the Post model called 'author' that allows us to access the user who created a post. The lazy=True parameter means that the related posts will be loaded from the database only when they are accessed, rather than being loaded immediately when the user is queried.
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
    ''''
    @staticmethod
    def get_reset_token(self,expires_sec=1800):
        s= Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'used_id':self.id}).decode('utf-8')
    
    def verify_reset_token(token):
        s= Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.load(token)['used_id']
        except:
            return None
        return User.query.get(user_id)
    '''
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except Exception:
            return None

        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"  
    
        
class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"