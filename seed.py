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
users.append(User(first_name='Johnathan', last_name='Booy'))
users.append(User(first_name='Regard', last_name='Booy', image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pastemagazine.com%2Ftv%2Fthe-50-best-cartoon-characters-of-all-time%2F&psig=AOvVaw1SYuCbb1NsA-xBlyoXb7Jb&ust=1664989410075000&source=images&cd=vfe&ved=0CAkQjRxqFwoTCJCPoYWHx_oCFQAAAAAdAAAAABAD'))
users.append(User(first_name='Megan', last_name='Mackay', image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pastemagazine.com%2Ftv%2Fthe-50-best-cartoon-characters-of-all-time%2F&psig=AOvVaw1SYuCbb1NsA-xBlyoXb7Jb&ust=1664989410075000&source=images&cd=vfe&ved=0CAkQjRxqFwoTCJCPoYWHx_oCFQAAAAAdAAAAABAI'))
users.append(User(first_name='Laura', last_name='Tsai',
             image_url='https://i.pinimg.com/550x/10/f9/37/10f937f2267cc07df2465b6d77b2973a.jpg'))

for user in users:
    db.session.add(user)

db.session.commit()
