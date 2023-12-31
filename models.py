from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    text = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='feedback')
## creatd  relatinoship for feedback and specific user 

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name = first_name, last_name = last_name)
    
    ## Take password in, hases into unicode utf8 string and then create new user instance

    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()
##Need to put in a form later for the model
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u 
        else:
            return False
