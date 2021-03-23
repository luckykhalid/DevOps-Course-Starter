from todo_app.data.TrelloApi import TrelloApi
from todo_app.app import create_app
import os
import pytest
from threading import Thread


@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    board_id = TrelloApi.create_board_temp()
    os.environ['BOARD_ID'] = board_id
    # construct the new application
    app = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    TrelloApi.delete_board(board_id)
