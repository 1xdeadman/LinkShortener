import pytest

from flask import Flask
from pymongo import MongoClient
from pymongo.collection import Collection

from src import create_app
from src.db import add_new_url, remove_url_by_short_url, get_long_url


@pytest.fixture(scope='function')
def app():
    test_app = create_app()
    yield test_app


@pytest.fixture(scope='function')
def urls():
    client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
    collection = client['delis_info']['urls']
    client.drop_database('delis_info')
    yield collection
    client.drop_database('delis_info')


@pytest.fixture
def client(app):
    return app.test_client()


def test_add_url(urls: Collection, app: Flask):
    with app.app_context():
        add_res1 = add_new_url("longTEST1")
        add_res2 = add_new_url("longTEST2")
        assert add_res1 is not None
        assert add_res2 is not None

        test_entity1 = urls.find_one({'long_url': "longTEST1"})
        test_entity2 = urls.find_one({'long_url': "longTEST2"})
        assert test_entity1 is not None
        assert test_entity2 is not None
        assert test_entity1['_id'].binary == add_res1
        assert test_entity2['_id'].binary == add_res2


def test_remove_url(urls: Collection, app: Flask):
    with app.app_context():
        add_res1 = add_new_url("longTEST1")
        add_res2 = add_new_url("longTEST2")

        remove_res_1 = remove_url_by_short_url(add_res1)
        test_entity1 = urls.find_one({'long_url': "longTEST1"})
        test_entity2 = urls.find_one({'long_url': "longTEST2"})
        assert test_entity1 is None
        assert test_entity2['long_url'] == "longTEST2"

        remove_res_2 = remove_url_by_short_url(add_res2)
        test_entity2 = urls.find_one({'long_url': "longTEST2"})
        assert test_entity2 is None

        remove_res_1 = remove_url_by_short_url(add_res1)
        assert remove_res_1 is False


def test_get_long_url(urls: Collection, app: Flask):
    with app.app_context():
        add_res1 = add_new_url("longTEST1")
        add_res2 = add_new_url("longTEST2")
        get_res1 = get_long_url(add_res1)
        get_res2 = get_long_url(add_res2)
        assert "longTEST1" == get_res1
        assert "longTEST2" == get_res2
