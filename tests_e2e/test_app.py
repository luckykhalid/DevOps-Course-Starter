import time
from todo_app.data.TrelloApi import TrelloApi
from todo_app.app import create_app
from selenium import webdriver
import os
import pytest
from threading import Thread
from dotenv import find_dotenv, load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope='module')
def app_with_temp_board():
    # Use real config instead of the 'test' version
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    # Create the new temp board & update the board id environment variable
    TrelloApi.init()
    TrelloApi.create_temp_board_set_env()

    # construct the new application
    app = create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: app.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    print(f'Board Id before deleting is: {TrelloApi.BOARD_ID}')
    TrelloApi.delete_borad_current()


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
    driver.implicitly_wait(10)

    task_name = 'This is an automated task 1.'
    input_task_title = driver.find_element_by_id("title")
    input_task_title.send_keys(task_name)
    # input_task_title.send_keys(Keys.ENTER)
    input_task_title.submit()
    time.sleep(5)
    assert task_name in driver.page_source
    #WebDriverWait(driver, 15)
    #element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("someId"))
    # is_disappeared = WebDriverWait(driver, 30, 1, (ElementNotVisibleException)).\
    #until_not(lambda x: x.find_element_by_id("someId").is_displayed())
