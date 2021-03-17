from todo_app.data.Status import Status
from todo_app.data.FieldNames import FieldNames
from todo_app.utils import change_key_in_list_of_dicts, join_lists_of_dicts
import requests
import os


class TrelloApi:
    """Trello API Calls."""
    TRELLO_KEY = os.environ.get('TRELLO_KEY')
    if not TRELLO_KEY:
        raise ValueError(
            "No TRELLO_KEY set for Trello API calls. Did you follow the setup instructions?")

    TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
    if not TRELLO_TOKEN:
        raise ValueError(
            "No TRELLO_TOKEN set for Trello API calls. Did you follow the setup instructions?")

    BOARD_ID = os.environ.get('BOARD_ID')
    if not TRELLO_TOKEN:
        raise ValueError(
            "No BOARD_ID set for Trello API calls. Did you follow the setup instructions?")

    LIST_TODO_ID = None
    LIST_DOING_ID = None
    LIST_DONE_ID = None

    PARAMS_KEY_TOKEN = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}
    URL_ROOT = 'https://api.trello.com/1/'

    PARAMS_GET_CARDS_FIELDS = {
        FieldNames.FIELDS: f'{FieldNames.NAME},{FieldNames.LIST_ID},{FieldNames.DATE_LAST_ACTIVITY}'}
    PARAMS_GET_CARDS = PARAMS_KEY_TOKEN | PARAMS_GET_CARDS_FIELDS
    URL_GET_CARDS = f'{URL_ROOT}boards/{BOARD_ID}/cards'

    PARAMS_GET_LISTS_FIELDS = {
        FieldNames.FIELDS: f'{FieldNames.NAME},idBoard'}
    PARAMS_GET_LISTS = PARAMS_KEY_TOKEN | PARAMS_GET_LISTS_FIELDS
    URL_GET_LISTS = f'{URL_ROOT}boards/{BOARD_ID}/lists'

    URL_CARDS = f'{URL_ROOT}cards'

    LISTS = None

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
