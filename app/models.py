#!flask/bin/python
# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from . import login_manager


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    nickname = db.Column(db.String(100), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.int)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), index=True)
    body = db.Column(db.Text)
    markdown_resource = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
    edit_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_published = db.Column(db.Boolean)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'commnents'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
    email = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
