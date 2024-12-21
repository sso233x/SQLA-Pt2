from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

#Create User model
class User(db.Model):
    """User."""
    
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False,)
    last_name = db.Column(db.String(30),
                          nullable=False,)
    image_url = db.Column(db.String(200),
                          nullable=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False,)
    content = db.Column(db.String(1000),
                        nullable=False,)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP'))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        return f"<Post {self.title}>"