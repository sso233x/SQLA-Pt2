"""Blogly application."""
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    """Redirect to list of users"""
    return redirect('/users')

@app.route('/users') 
def show_users():
    users = User.query.all()
    return render_template("base.html", users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_users():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form.get("image_url")

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')

    return render_template("form.html")

@app.route('/users/<int:user_id>')
def show_info(user_id):
    """Show info on a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.image_url = request.form.get("image_url")

        db.session.commit()
        return redirect('/users')

    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# POST ROUTES
@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def add_post(user_id):
    """Show form to add a post or handle form submission."""
    user = User.query.get_or_404(user_id)
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    
    return render_template("post-form.html", user=user)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details about a single post."""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template("post-detail.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    """Show form to edit a post or handle form submission."""
    post = Post.query.get_or_404(post_id)
    
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        return redirect(f"/posts/{post_id}")
    
    return render_template("post-edit.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")