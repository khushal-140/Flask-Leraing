

class Config:
    SECRET_KEY = '454454654ac4545454'# This is used to protect against CSRF (Cross-Site Request Forgery) attacks. It is a random string that should be kept secret in a production environment. In this example, it's just a placeholder value for demonstration purposes.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # This configures the database URI for SQLAlchemy. In this case, it specifies that we are using SQLite and the database file is named site.db. The triple slashes indicate a relative path to the database file.
    MAIL_SERVER='smtp.gamil.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True 
    MAIL_USERNAME='khushalbharat0@gmail.com'
    MAIL_PASSWORD='djdon'