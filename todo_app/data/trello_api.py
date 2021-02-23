import os
from todo_app.util import change_key_in_list_of_dicts, join_lists_of_dicts
import requests


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

    BOARD_ID = '60254e45c1345502980ecbf7'
    LIST_TODO_NAME = 'To Do'
    LIST_DOING_NAME = 'Doing'
    LIST_DONE_NAME = 'Done'
    LIST_TODO_ID = None
    LIST_DOING_ID = None
    LIST_DONE_ID = None

    PARAMS_KEY_TOKEN = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}

    PARAMS_GET_CARDS_FIELDS = {'fields': 'name,idList'}
    PARAMS_GET_CARDS = PARAMS_KEY_TOKEN | PARAMS_GET_CARDS_FIELDS
    URL_GET_CARDS = f'https://api.trello.com/1/boards/{BOARD_ID}/cards'

    PARAMS_GET_LISTS_FIELDS = {'fields': 'name,idBoard'}
    PARAMS_GET_LISTS = PARAMS_KEY_TOKEN | PARAMS_GET_LISTS_FIELDS
    URL_GET_LISTS = f'https://api.trello.com/1/boards/{BOARD_ID}/lists'

    URL_ADD_CARD = 'https://api.trello.com/1/cards'

    LISTS = None

    @classmethod
    def get_lists(cls):
        if cls.LISTS == None:
            lists = requests.get(
                cls.URL_GET_LISTS, params=cls.PARAMS_GET_CARDS).json()
            lists = change_key_in_list_of_dicts(lists, 'id', 'idList')
            cls.LISTS = change_key_in_list_of_dicts(lists, 'name', 'status')

        return cls.LISTS

    @classmethod
    def get_list_todo_id(cls):
        if cls.LIST_TODO_ID == None:
            lists = TrelloApi.get_lists()
            cls.LIST_TODO_ID = next(
                (item for item in lists if item['status'] == cls.LIST_TODO_NAME), None)['idList']

        return cls.LIST_TODO_ID

    @staticmethod
    def get_items_lists():
        cards = requests.get(
            TrelloApi.URL_GET_CARDS, params=TrelloApi.PARAMS_GET_CARDS).json()
        lists = TrelloApi.get_lists()
        items = join_lists_of_dicts(cards, lists, 'idList')
        return items

    @classmethod
    def add_item(cls, item_name):
        list_todo_id = TrelloApi.get_list_todo_id()

        payload = {
            'idList': list_todo_id,
            'name': item_name
        }
        new_card = requests.post(
            cls.URL_ADD_CARD, params=cls.PARAMS_KEY_TOKEN, json=payload).json()

        return new_card
