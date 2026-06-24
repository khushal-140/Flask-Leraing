
from flask import render_template, request, Blueprint
from flaskblog.models import Post

main= Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page=request.args.get('page',1,type=int) # This line retrieves the value of the "page" parameter from the query string of the request. If the "page" parameter is not present in the query string, it defaults to 1. The type=int argument ensures that the retrieved value is converted to an integer. This is used for pagination, allowing users to navigate through different pages of posts. 
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)   # This line queries the database to retrieve all the posts stored in the Post table. It uses SQLAlchemy's query interface to access the Post model and calls the all() method to get a list of all Post objects from the database. The retrieved posts are then stored in the posts variable, which can be passed to the template for rendering.
    return render_template('home.html',posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/contact')
def contact():
    return "<h1> contact us</h1>"