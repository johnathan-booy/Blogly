"""Seed file to make sample user data"""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
users = []
users.append(User(first_name='Johnathan', last_name='Booy',
             image_url="https://www.loudegg.com/wp-content/uploads/2020/10/Mickey-Mouse.jpg"))
users.append(User(first_name='Regard', last_name='Booy',
             image_url='https://www.loudegg.com/wp-content/uploads/2020/10/Bugs-Bunny.jpg'))
users.append(User(first_name='Megan', last_name='Mackay',
             image_url='https://www.loudegg.com/wp-content/uploads/2020/10/Tigger.jpg'))
users.append(User(first_name='Luke', last_name='Tsai',
             image_url='https://www.loudegg.com/wp-content/uploads/2020/10/Tommy-Pickles.jpg'))

for user in users:
    db.session.add(user)

db.session.commit()


# Add posts
posts = []
posts.append(Post(title='Bartimaeous',
             content='This is a very underrated book series.', user_id=1),)
posts.append(Post(title='Climate Change',
             content='We really should start doing something about this!', user_id=1))
posts.append(Post(title='Mila',
             content='Cutest dog in the world. Half golden retriever, half bernese mountain dog. Her favorite activities are running, panting anxiously and also drooling!', user_id=1))


for post in posts:
    db.session.add(post)

db.session.commit()
