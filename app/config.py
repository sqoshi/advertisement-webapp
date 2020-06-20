import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Set up database sqlalchemy"""
    cst = '?check_same_thread=False'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                            'app.db') + cst
    SQLALCHEMY_TRACK_MODIFICATIONS = False
