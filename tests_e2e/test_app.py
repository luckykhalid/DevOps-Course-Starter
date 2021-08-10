import time
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
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=options) as driver:
        yield driver


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


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
    driver.implicitly_wait(3)

    start_button_text = ".//a[contains(text(), 'Start')]"
    done_button_text = '.btn.btn-outline-secondary.btn-sm'
    restart_button_text = ".//a[contains(text(), 'Restart')]"
    delete_button_text = ".//a[contains(text(), 'Delete')]"

    # Test creating a new task and check if it exists on the web page
    task_name = 'This is an automated task 1.'
    input_task_title = driver.find_element_by_id("title")
    input_task_title.send_keys(task_name)
    input_task_title.submit()
    time.sleep(1)
    assert task_name in driver.page_source
    #elem = driver.find_element_by_xpath(f'//th[contains(text(), "{task_name}")]')
    #assert elem != None

    # Navigate to the ToDo Tab
    tab_todo = driver.find_element_by_id("nav-todo-tab")
    tab_todo.click()
    time.sleep(1)
    # Start the new ToDo task
    start_button = driver.find_element_by_xpath(start_button_text)
    start_button.click()
    time.sleep(1)
    assert task_name in driver.page_source

    # Navigate to the Doing Tab
    tab_doing = driver.find_element_by_id("nav-doing-tab")
    tab_doing.click()
    time.sleep(1)
    # Complete the Doing task
    done_button = driver.find_element_by_css_selector(
        done_button_text)
    done_button.click()
    time.sleep(1)
    assert task_name in driver.page_source

    # Page automaticlaly shows Done tasks so restart the Done task
    restart_button = driver.find_element_by_xpath(restart_button_text)
    restart_button.click()
    time.sleep(1)
    assert task_name in driver.page_source

    # Navigate to the Doing Tab
    tab_doing = driver.find_element_by_id("nav-doing-tab")
    tab_doing.click()
    time.sleep(1)
    # Delete the Doing task
    delete_button = driver.find_element_by_xpath(delete_button_text)
    delete_button.click()
    time.sleep(1)
    assert task_name not in driver.page_source

    # Navigate to the All Tab
    tab_all = driver.find_element_by_id("nav-all-tab")
    tab_all.click()
    time.sleep(1)
