from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import JSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from flask import current_app

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.UnicodeText, index=True, unique=True)
    name = db.Column(db.UnicodeText)
    password_hash = db.Column(db.String(64))
    group = db.Column(db.UnicodeText)
    image = db.Column(db.UnicodeText)

    def __init__(self, username):
        self.username = username
        self.group = username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Invite(db.Model):
    __tablename__ = 'invites'
    id = db.Column(db.Integer, primary_key=True)
    invite_from = db.Column(db.UnicodeText)
    invite_to = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<Invite from %r to %r>' % (self.invite_from, self.invite_to)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, index=True)
    meals = db.relationship('Meal', backref='category')

    def __repr__(self):
        return '<Category %r>' % self.name


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, index=True)
    group = db.Column(db.UnicodeText)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    client_id = db.Column(db.String(36)) # UUID
    revision = db.Column(db.Integer)
    color = db.Column(db.UnicodeText)
    image = db.Column(db.UnicodeText)
    description = db.Column(db.UnicodeText)

    def __repr__(self):
        return '<Meal: %s, Group: %s>' % (self.name, self.group)

class ColorLegend(db.Model):
    __tablename__ = 'colorlegend'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.UnicodeText)
    group = db.Column(db.UnicodeText)
    legend = db.Column(db.UnicodeText)