"""Models for Blogly."""
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(), nullable=True)

    posts = db.relationship('Post', back_populates="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def posts_quantity(self):
        return len(self.posts)

    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now)
    user_id = db.Column(db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

    @property
    def timestamp(self):
        return self.created_at.strftime("%a %b %d, %Y at %I:%M %p")

    @property
    def tags_quantity(self):
        return len(self.tags)

    def __repr__(self):
        return f'<Post id={self.id} user={self.user.full_name} title={self.title} created_at={self.created_at}>'


class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)

    def __repr__(self):
        return f"<PostTag post_id={self.post_id} tags_id={self.tag_id}>"


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(18), nullable=False, unique=True)

    @property
    def posts_quantity(self):
        return len(self.posts)

    def __repr__(self):
        return f"<Tag name={self.name}>"
