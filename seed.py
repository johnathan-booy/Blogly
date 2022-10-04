"""Seed file to make sample user data"""

from models import User, db
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
