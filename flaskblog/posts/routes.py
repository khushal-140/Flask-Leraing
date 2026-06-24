
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts= Blueprint('posts',__name__)






@posts.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():      
        post=Post(title=form.title.data, content=form.content.data, author=current_user) # This line creates a new Post object with the title and content obtained from the post creation form, and it also associates the post with the current user (the author). The Post class is defined in the models.py file and represents a blog post in the database. The title and content are taken directly from the form data, while the author is set to the current_user, which is provided by Flask-Login and represents the currently logged-in user.
        db.session.add(post) # This line adds the newly created Post object to the current database session. It prepares the post to be inserted into the database when the session is committed.
        db.session.commit() # This line commits the current database session, which means that all changes made to the database (such as adding the new post) will be saved to the database.
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))     
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')      
    
@posts.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id) # This line queries the database to retrieve a post with the specified post_id. It uses SQLAlchemy's query interface to access the Post model and calls the get_or_404 method, which attempts to retrieve the post with the given ID. If a post with that ID exists, it will return a Post object; otherwise, it will raise a 404 error, indicating that the requested resource was not found. The retrieved post is then stored in the post variable, which can be passed to the template for rendering
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')
    
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
