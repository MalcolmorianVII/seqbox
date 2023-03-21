import pytest
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture
def supply_dict_info_per_sample(dict_info):
    return dict_info

@pytest.fixture
def supply_elution_info(elution_info):
    """
    Supply the following info:
        (1) Elution info(dict???)
        (2) Db connection
        (3) 
    """
    return elution_info

@pytest.fixture
def supply_db_conn():
    app = Flask(__name__) # Create a Flask app instance
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    return db

def db_connector(test_fxn):
    def test_fxn_wrapper(*args,**kwargs):
        app = Flask(__name__) # Create a Flask app instance
        app.config.from_object(Config)
        db = SQLAlchemy(app)
        test_fxn(*args,**kwargs)

    return test_fxn_wrapper