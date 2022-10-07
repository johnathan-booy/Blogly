"""Blogly application."""
from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import Post, db, connect_db, User

app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Flask Debug Toolbar
app.config['SECRET_KEY'] = "12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def show_home_page():
    """Shows the most recent blog posts"""
    posts = Post.query.limit(5).all()
    return render_template('index.html', posts=posts)


@app.route('/users')
def show_users():
    """List all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def show_create_user_form():
    """Shows an add form for users"""
    return render_template('create-user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Add user to db from form submission"""
    first_name = request.form['first_name'].title()
    last_name = request.form['last_name'].title()
    image_url = request.form['image_url']

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    "Show details about a specific user"
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user-details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Shows an edit form for selected user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edit user on db from form submission"""
    first_name = request.form['first_name'].title()
    last_name = request.form['last_name'].title()
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user from db"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show form where a user can add a new post"""
    user = User.query.get_or_404(user_id)
    return render_template('add-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Show form where a user can add a new post"""
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)

    if title and content:
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{user_id}')
    else:
        if not title:
            flash('Posts must include a title!')
        if not content:
            flash('Posts must include content!')
        return redirect(f'/users/{user_id}/posts/new')


@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Show all details for a specific post"""
    post = Post.query.get(post_id)
    return render_template('post-details.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post from db"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Display a form where users can edit a specific post"""
    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Send edited post to update the db"""
    post = Post.query.get(post_id)
    title = request.form['title']
    content = request.form['content']

    if title:
        post.title = title

    if content:
        post.content = content

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
