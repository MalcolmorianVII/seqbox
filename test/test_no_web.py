import os
from app import db
from config import PASSWORD,PORT,USER,DB_POSTGRES


def create_it():
    db.create_all()


def wipe_it_and_create_it():
    # putting this assertion here to stop me from wiping the non-test database
    #postgresql://user:password@localhost:5432/database_name

    # SQLALCHEMY_DATABASE_URI = 'postgresql:///test_sq_service_db:'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{DB_POSTGRES}'
    assert SQLALCHEMY_DATABASE_URI.split('/')[-1].startswith('test')
    
    db.drop_all()
    db.create_all()


wipe_it_and_create_it()
# create_it()
