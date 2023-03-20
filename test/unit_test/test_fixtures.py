import pytest

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
def supply_db_conn(con):
    return con