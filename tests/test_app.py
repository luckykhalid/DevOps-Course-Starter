from todo_app.data.TrelloApi import TrelloApi
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
        print('Before yeild')
        yield client
        print('After yeild')


@patch('requests.get')
def test_index_page_mocked(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    print('Executing test')
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')


def mock_get_lists(url, params):
    mock_file = None

    if url == TrelloApi.URL_GET_LISTS:
        mock_file = FieldNames.LISTS
    elif url == TrelloApi.URL_GET_CARDS:
        mock_file = FieldNames.CARDS
    else:
        return None

    response = Mock()
    with open(f'{os.getcwd()}/tests/data/{mock_file}.json') as json_file:
        response.json.return_value = json.load(json_file)
    return response
