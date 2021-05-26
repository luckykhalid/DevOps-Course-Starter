from todo_app.data.Status import Status
from todo_app.data.FieldNames import FieldNames
from todo_app.utils import change_key_in_list_of_dicts, join_lists_of_dicts
import requests
import os
import uuid


class TrelloApi:

    URL_ROOT = 'https://api.trello.com/1/'

    @classmethod
    def init(cls):
        cls.LIST_TODO_ID = None
        cls.LIST_DOING_ID = None
        cls.LIST_DONE_ID = None
        cls.LISTS = None

        """Trello API Calls."""
        cls.TRELLO_KEY = os.environ.get('TRELLO_KEY')
        if not cls.TRELLO_KEY:
            raise ValueError(
                "No TRELLO_KEY set for Trello API calls. Did you follow the setup instructions?")

        cls.TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
        if not cls.TRELLO_TOKEN:
            raise ValueError(
                "No TRELLO_TOKEN set for Trello API calls. Did you follow the setup instructions?")

        cls.BOARD_ID = os.environ.get('BOARD_ID')
        print(f'Board Id being set is: {cls.BOARD_ID}')
        if not cls.TRELLO_TOKEN:
            raise ValueError(
                "No BOARD_ID set for Trello API calls. Did you follow the setup instructions?")

        cls.PARAMS_KEY_TOKEN = {
            'key': cls.TRELLO_KEY, 'token': cls.TRELLO_TOKEN}

        cls.PARAMS_GET_CARDS_FIELDS = {
            FieldNames.FIELDS: f'{FieldNames.NAME},{FieldNames.LIST_ID},{FieldNames.DATE_LAST_ACTIVITY}'}
        cls.PARAMS_GET_CARDS = cls.PARAMS_KEY_TOKEN | cls.PARAMS_GET_CARDS_FIELDS
        cls.URL_GET_CARDS = f'{cls.URL_ROOT}{FieldNames.BOARDS}/{cls.BOARD_ID}/{FieldNames.CARDS}'

        cls.PARAMS_GET_LISTS_FIELDS = {
            FieldNames.FIELDS: f'{FieldNames.NAME},{FieldNames.BOARD_ID}'}
        cls.PARAMS_GET_LISTS = cls.PARAMS_KEY_TOKEN | cls.PARAMS_GET_LISTS_FIELDS

        cls.URL_GET_LISTS = f'{cls.URL_ROOT}{FieldNames.BOARDS}/{cls.BOARD_ID}/{FieldNames.LISTS}'
        cls.URL_CARDS = f'{cls.URL_ROOT}{FieldNames.CARDS}'
        cls.URL_BOARDS = f'{cls.URL_ROOT}{FieldNames.BOARDS}'

    @classmethod
    def get_lists(cls) -> list:
        if cls.LISTS == None:
            lists = requests.get(
                cls.URL_GET_LISTS, params=cls.PARAMS_GET_CARDS).json()
            lists = change_key_in_list_of_dicts(
                lists, FieldNames.ID, FieldNames.LIST_ID)
            cls.LISTS = change_key_in_list_of_dicts(
                lists, FieldNames.NAME, FieldNames.STATUS)

        return cls.LISTS

    @classmethod
    def get_list_id(cls, list_name) -> str:
        lists = cls.get_lists()
        return next((item for item in lists if item[FieldNames.STATUS] == list_name), None)[FieldNames.LIST_ID]

    @classmethod
    def get_list_id_todo(cls) -> str:
        if cls.LIST_TODO_ID == None:
            cls.LIST_TODO_ID = cls.get_list_id(Status.TODO.value)

        return cls.LIST_TODO_ID

    @classmethod
    def get_list_id_doing(cls) -> str:
        if cls.LIST_DOING_ID == None:
            cls.LIST_DOING_ID = cls.get_list_id(Status.DOING.value)

        return cls.LIST_DOING_ID

    @classmethod
    def get_list_id_done(cls) -> str:
        if cls.LIST_DONE_ID == None:
            cls.LIST_DONE_ID = cls.get_list_id(Status.DONE.value)

        return cls.LIST_DONE_ID

    @staticmethod
    def get_items_lists() -> list:
        cards = requests.get(
            TrelloApi.URL_GET_CARDS, params=TrelloApi.PARAMS_GET_CARDS).json()
        lists = TrelloApi.get_lists()
        items = join_lists_of_dicts(cards, lists, FieldNames.LIST_ID)
        return items

    @classmethod
    def add_item(cls, item_name):
        list_todo_id = TrelloApi.get_list_id_todo()

        payload = {
            FieldNames.LIST_ID: list_todo_id,
            FieldNames.NAME: item_name
        }
        new_card = requests.post(
            cls.URL_CARDS, params=cls.PARAMS_KEY_TOKEN, json=payload).json()

        return new_card

    @staticmethod
    def delete_item(item_id):
        url = f'{TrelloApi.URL_CARDS}/{item_id}'
        response = requests.delete(
            url=url, params=TrelloApi.PARAMS_KEY_TOKEN)
        return response

    @staticmethod
    def update_item_list(item_id, list_id):
        url = f'{TrelloApi.URL_CARDS}/{item_id}'

        payload = {
            FieldNames.LIST_ID: list_id
        }
        response = requests.put(
            url=url, params=TrelloApi.PARAMS_KEY_TOKEN, json=payload).json()
        return response

    @staticmethod
    def doing_item(item_id):
        list_id = TrelloApi.get_list_id_doing()
        response = TrelloApi.update_item_list(item_id, list_id)
        return response

    @staticmethod
    def done_item(item_id):
        list_id = TrelloApi.get_list_id_done()
        response = TrelloApi.update_item_list(item_id, list_id)
        return response

    @staticmethod
    def create_board(board_name):
        params = TrelloApi.PARAMS_KEY_TOKEN | {FieldNames.NAME: board_name}
        #print(f'URL: {TrelloApi.URL_BOARDS} , PARAMS: {params}')
        response = requests.post(
            url=TrelloApi.URL_BOARDS, params=params).json()
        return response

    @staticmethod
    def create_temp_board_set_env():
        response = TrelloApi.create_board(uuid.uuid4().hex)
        os.environ['BOARD_ID'] = response[FieldNames.ID]
        return response[FieldNames.ID]

    @staticmethod
    def delete_board(board_id):
        url = f'{TrelloApi.URL_BOARDS}/{board_id}'
        response = requests.delete(
            url=url, params=TrelloApi.PARAMS_KEY_TOKEN)
        return response

    @classmethod
    def delete_borad_current(cls):
        return cls.delete_board(cls.BOARD_ID)
