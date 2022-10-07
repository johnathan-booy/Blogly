"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from imghdr import what

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(), nullable=True)

    posts = db.relationship('Post', cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        return f'<Post id={self.id} user={self.user.full_name} title={self.title} created_at={self.created_at}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.now)
    user_id = db.Column(db.ForeignKey('users.id'))

    user = db.relationship('User')

    @property
    def timestamp(self):
        return self.created_at.strftime("%a %b %d, %Y at %I:%M %p")
