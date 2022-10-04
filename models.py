"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

missing_user_image_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fpixabay.com%2Fvectors%2Fblank-profile-picture-mystery-man-973460%2F&psig=AOvVaw0QevVd3crsKhFu-CGDtXhC&ust=1664988488925000&source=images&cd=vfe&ved=0CAkQjRxqFwoTCMjpktSDx_oCFQAAAAAdAAAAABAD"


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
    image_url = db.Column(db.String(), nullable=True,
                          default=missing_user_image_url)
