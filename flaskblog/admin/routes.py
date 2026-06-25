from flask import render_template, abort
from flask_login import login_required, current_user
from flaskblog.admin import admin
from flaskblog.models import User, Post



@admin.route("/admin")
@login_required
def dashboard():

    if not current_user.is_admin:
        abort(403)

    total_users = User.query.count()
    total_posts = Post.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()
    users = User.query.order_by(User.id).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_posts=total_posts,
        total_admins=total_admins,
         users=users
    )