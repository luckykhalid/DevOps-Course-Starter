from todo_app.data.TrelloApi import TrelloApi
from todo_app.data.FieldNames import FieldNames
import os
from unittest.mock import patch, Mock
import json



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