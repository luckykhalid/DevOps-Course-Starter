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


@patch('requests.get')
def test_index_page_mocked(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    assert response.status_code == 200
    assert b'I completed my Lunch, Brilliant! :)' in response.data
    assert b'This is added from Mongo DB website' in response.data
    assert b'Happy New Item' in response.data


@patch('requests.delete')
def test_delete_board(mock_delete_requests, client):
    mock_delete_requests.side_effect = mock_delete_board
    board_id = 'A Test Board'

    response = MongoDbApi.delete_board(board_id)

    assert response.status_code == 200


def mock_get_lists(url, params):
    mock_file = None

    if url == MongoDbApi.URL_GET_LISTS:
        mock_file = FieldNames.LISTS
    elif url == MongoDbApi.URL_GET_CARDS:
        mock_file = FieldNames.CARDS
    else:
        return None

    response = Mock()
    with open(f'{os.getcwd()}/tests/data/{mock_file}.json') as json_file:
        response.json.return_value = json.load(json_file)
    return response





def mock_delete_board(url, params):
    response = Mock()
    with open(f'{os.getcwd()}/tests/data/delete_board.json') as json_file:
        response.json.return_value = json.load(json_file)
        response.status_code = 200
    return response
