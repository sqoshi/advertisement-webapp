from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    """Forum user model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    @login.user_loader
    def load_user(id):
        """
        :return: User row by user id
        """
        return User.query.get(int(id))

    def set_password(self, password):
        """
        save as hash
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        hash check
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        """
        Generate avatar icon (const)
        :param size:
        :return:
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Announcement(db.Model):
    """Announcement model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    body = db.Column(db.String(140))
    price = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Ann {}>'.format(self.body)

    def getAnnouncesAll(self):
        """
        :return: all annonces in database
        """
        return self.root.findall("./anns")

    def remove_Ann(self, idx):
        """
        removes announce by id
        :param idx: Announce.id
        """
        for ann in self.root.findall('./anime'):
            if ann[1].text == idx:
                self.root.remove(ann)
