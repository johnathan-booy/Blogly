"""Blogly application."""
from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import Post, User, Tag, PostTag, db, connect_db

app = Flask(__name__)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

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
    tags = Tag.query.limit(10).all()
    return render_template('create-post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Show form where a user can add a new post"""
    title = request.form['title']
    content = request.form['content']
    tags = [int(id) for id in request.form.getlist('tags')]
    user = User.query.get_or_404(user_id)

    if title and content:
        post = Post(title=title, content=content, user_id=user_id)
        post.tags = Tag.query.filter(Tag.id.in_(tags)).all()
        db.session.add(post)
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
    post = Post.query.get_or_404(post_id)
    return render_template('post-details.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post from db"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Display a form where users can edit a specific post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.limit(10).all()
    return render_template('edit-post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Send edited post to update the db"""
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']
    tags = [int(id) for id in request.form.getlist('tags')]

    if title:
        post.title = title

    if content:
        post.content = content

    post.tags = Tag.query.filter(Tag.id.in_(tags)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/tags')
def show_tags():
    """Show a list of all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show a list of all posts that belong to the specified"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag-details.html', tag=tag, posts=posts)


@app.route('/tags/new')
def show_create_tag_form():
    """Show a form that allows users to add a new tag to the website"""
    posts = Post.query.limit(10).all()
    return render_template('create-tag.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Add a new tag to the database"""
    name = request.form['name'].lower()
    tag = Tag(name=name)
    posts = [int(id) for id in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(posts)).all()
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag.id}')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag from the database"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show a from to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.limit(10).all()
    return render_template('edit-tag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Edit a tag in the database"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    posts = [int(id) for id in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(posts)).all()
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
