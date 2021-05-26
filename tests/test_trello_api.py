from todo_app.data.TrelloApi import TrelloApi
from todo_app.data.FieldNames import FieldNames
import os
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch, Mock
import json



def test_create_delete_board():
    # Use real config instead of the 'test' version
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    TrelloApi.init()
    board_id = TrelloApi.create_temp_board_set_env()
    assert board_id
    assert os.environ.get('BOARD_ID') == board_id
    response = TrelloApi.delete_board(board_id)
    assert response.ok


@patch('requests.post')
def test_create_board(mock_post_requests):
    mock_post_requests.side_effect = mock_create_board
    board_name = 'A New Test Board'

    new_board = TrelloApi.create_board(board_name)

    assert new_board[FieldNames.ID] == '6059ec106aec31192a803aa6'
    assert new_board[FieldNames.NAME] == board_name

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