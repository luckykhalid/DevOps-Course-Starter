from todo_app.data.TrelloApi import TrelloApi
from dotenv import find_dotenv, load_dotenv


def test_create_delete_board():
    # Use real config instead of the 'test' version
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    TrelloApi.init()
    board_id = TrelloApi.create_board_temp()
    assert board_id
    response = TrelloApi.delete_board(board_id)
    assert response.ok
