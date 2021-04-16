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
        yield client


@patch('requests.get')
def test_index_page_mocked(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    assert response.status_code == 200
    assert b'I completed my Lunch, Brilliant! :)' in response.data
    assert b'This is added from Trello website' in response.data
    assert b'Happy New Item' in response.data


@patch('requests.post')
def test_create_board(mock_post_requests, client):
    mock_post_requests.side_effect = mock_create_board
    board_name = 'A New Test Board'

    new_board = TrelloApi.create_board(board_name)

    assert new_board[FieldNames.ID] == '6059ec106aec31192a803aa6'
    assert new_board[FieldNames.NAME] == board_name


@patch('requests.delete')
def test_delete_board(mock_delete_requests, client):
    mock_delete_requests.side_effect = mock_delete_board
    board_id = 'A Test Board'

    response = TrelloApi.delete_board(board_id)

    assert response.status_code == 200


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


def mock_create_board(url, params):
    mock_file = None

    if url == TrelloApi.URL_BOARDS:
        mock_file = 'new_board'
    else:
        return None

    response = Mock()
    with open(f'{os.getcwd()}/tests/data/{mock_file}.json') as json_file:
        new_board = json.load(json_file)
        new_board[FieldNames.NAME] = params[FieldNames.NAME]
        response.json.return_value = new_board
    return response


def mock_delete_board(url, params):
    response = Mock()
    with open(f'{os.getcwd()}/tests/data/delete_board.json') as json_file:
        response.json.return_value = json.load(json_file)
        response.status_code = 200
    return response
