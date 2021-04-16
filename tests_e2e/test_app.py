from todo_app.data.TrelloApi import TrelloApi
from todo_app.app import create_app
from selenium import webdriver
import os
import pytest
from threading import Thread
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(scope='module')
def app_with_temp_board():
    # Use real config instead of the 'test' version
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    # Create the new board & update the board id environment variable
    TrelloApi.init()
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


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
