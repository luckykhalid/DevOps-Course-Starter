from todo_app.data.MongoDbApi import MongoDbApi
from todo_app.data.FieldNames import FieldNames
from todo_app.app import create_app
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch, Mock
import json
import os
import pytest


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


@patch('pymongo.collection.Collection.find')
def test_index_page_mocked(mock_find, client):
    # Replace call to requests.get(url) with our own function
    mock_find.side_effect = mock_get_items
    response = client.get('/')
    assert response.status_code == 200
    assert b'I completed my Lunch, Brilliant! :)' in response.data
    assert b'This is added from Mongo DB website' in response.data
    assert b'Happy New Item' in response.data


def mock_get_items():
    items = Mock()
    with open(f'{os.getcwd()}/tests/data/items.json') as json_file:
        items = json.load(json_file)
    return items
