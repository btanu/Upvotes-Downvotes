from os import stat
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class Pitch(db.Model):

    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
    posted = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id')) #tels alchemy foreign key and is the primary key of roles
    up_vote = db.relationship('UpVote',backref = 'post',lazy = "dynamic")
    comment = db.relationship('Comments',backref = 'post',lazy = "dynamic")
    down_vote = db.relationship('DownVote',backref = 'post',lazy = "dynamic")

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches_category(cls,category_id):
        categoryPitches = Pitch.query.filter_by(category_id = category_id).order_by(Pitch.posted.desc())
        return categoryPitches

    @classmethod
    def get_my_posts(cls, user_id):
        my_posts = Pitch.query.filter_by(user_id = user_id).order_by(Pitch.posted.desc())
        return my_posts

class User(UserMixin, db.Model): #arg helps connect  to db
    __tablename__ = 'users' #table name
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique = True, index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255)) 
    pitch = db.relationship('Pitch',backref = 'user',lazy = "dynamic")

    @property #create write only class property password
    def password(self):
        raise AttributeError('You cannot read the password attribute') #we raise an attribute error to block access to the password property

    @password.setter
    def password(self, password):  #save hash to pass_secure column in database
        self.pass_secure = generate_password_hash(password)
    
    def verify_password(self, password): #takes pass hashes it and checks if it is the same
        return check_password_hash(self.pass_secure, password)

    @staticmethod
    def verify_email(email):
        return User.query.filter_by(email = email).first()

    def __repr__(self):
        return f'User {self.username}'

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255), unique=True)
    pitch = db.relationship('Pitch',backref = 'category',lazy = "dynamic")

    def save_category(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_categories():
        return Category.query.all()

    def __repr__(self):
        return f'User {self.category}'

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    posted = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id')) #tels alchemy foreign key and is the primary key of roles

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comments.query.filter_by(pitch_id = pitch_id).all()
        return comments

    @classmethod
    def get_my_comments(cls, user_id):
        my_comments = Comments.query.filter_by(id = user_id).first()
        return my_comments

    def __repr__(self):
        return f'User {self.comment}'

class UpVote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id')) #tels alchemy foreign key and is the primary key of roles

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_vote(cls, post_id):
        upvotes = UpVote.query.filter_by(post_id = post_id).all()
        return upvotes

    @classmethod
    def get_my_vote(cls, user_id):
        my_votes = User.query.filter_by(id = user_id).all()
        return my_votes

    def __repr__(self):
        return f'User {self.id}'

class DownVote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id')) #tels alchemy foreign key and is the primary key of roles

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_vote(cls, post_id):
        downvotes = DownVote.query.filter_by(post_id = post_id).all()
        return downvotes

    
    @classmethod
    def get_my_vote(cls, user_id):
        my_votes = User.query.filter_by(id = user_id).all()
        return my_votes

    def __repr__(self):
        return f'User {self.id}'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))