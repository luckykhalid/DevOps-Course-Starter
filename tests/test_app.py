from todo_app.app import create_app
import pytest
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch, Mock


TEST_BOARD_ID = '60254e45c1345502980ecbf7'


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


def test_index_page(client):
    response = client.get('/')


@patch('requests.get')
def test_index_page_mocked(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')


def mock_get_lists(url, params):
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = 'sample_trello_lists_response'
        return response
    return None
