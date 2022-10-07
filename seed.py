"""Seed file to make sample user data"""
from app import app
from models import PostTag, User, Post, Tag, db

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
users = [
    (User(first_name='Johnathan', last_name='Booy',
          image_url="https://www.loudegg.com/wp-content/uploads/2020/10/Mickey-Mouse.jpg")),
    (User(first_name='Regard', last_name='Booy',
          image_url='https://www.loudegg.com/wp-content/uploads/2020/10/Bugs-Bunny.jpg')),
    (User(first_name='Megan', last_name='Mackay',
          image_url='https://www.loudegg.com/wp-content/uploads/2020/10/Tigger.jpg')),
    (User(first_name='Luke', last_name='Tsai',
          image_url='https://www.loudegg.com/wp-content/uploads/2020/10/Tommy-Pickles.jpg'))]

for user in users:
    db.session.add(user)

db.session.commit()


# Add posts
posts = [
    (Post(title='Bartimaeous',
          content='This is a very underrated book series.', user_id=1)),
    (Post(title='Climate Change',
          content='We really should start doing something about this!', user_id=1)),
    (Post(title='Mila',
          content='Cutest dog in the world. Half golden retriever, half bernese mountain dog. Her favorite activities are running, panting anxiously and also drooling!', user_id=3)),
    (Post(title='User Experience Report',
          content='This website is shit!', user_id=2)),
    (Post(title='Juvenile Perspective',
          content='Wahhhhhhhhhhh', user_id=4))]

for post in posts:
    db.session.add(post)

db.session.commit()


# Add tags
tags = [
    Tag(name='opinion'),
    Tag(name='fact'),
    Tag(name='relevant')
]

for tag in tags:
    db.session.add(tag)

db.session.commit()

# Add post <-> tag relationships
post_tags = [
    PostTag(post_id=1, tag_id=1),
    PostTag(post_id=2, tag_id=2),
    PostTag(post_id=2, tag_id=3),
    PostTag(post_id=3, tag_id=2),
    PostTag(post_id=4, tag_id=1),
    PostTag(post_id=5, tag_id=1)
]

for post_tag in post_tags:
    db.session.add(post_tag)

db.session.commit()
