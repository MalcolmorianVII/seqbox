import os
basedir = os.path.abspath(os.path.dirname(__file__))

PASSWORD = os.environ['PASSWORD']
USER = os.environ['USER']
PORT = os.environ['PORT']
DB_POSTGRES = os.environ['DB_POSTGRES']

class Config(object):
    """[Configuration file]
    """

    # Flask-SQLAlchemy: Initialize
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DB_POSTGRES}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
