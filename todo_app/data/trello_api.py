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
    LIST_TODO_ID = '60254e45c1345502980ecbf8'
    LIST_DONE_ID = '60254e45c1345502980ecbfa'

    PARAMS_ALL = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}

    PARAMS_GET_CARDS_FIELDS = {'fields': 'name,idList'}
    PARAMS_GET_CARDS = PARAMS_ALL | PARAMS_GET_CARDS_FIELDS
    URL_GET_CARDS = f'https://api.trello.com/1/boards/{BOARD_ID}/cards'

    PARAMS_GET_LISTS_FIELDS = {'fields': 'name,idBoard'}
    PARAMS_GET_LISTS = PARAMS_ALL | PARAMS_GET_LISTS_FIELDS
    URL_GET_LISTS = f'https://api.trello.com/1/boards/{BOARD_ID}/lists'

    LISTS = None

    @classmethod
    def get_lists(cls):
        if cls.LISTS == None:
            lists = requests.get(
                cls.URL_GET_LISTS, params=cls.PARAMS_GET_CARDS).json()
            lists = change_key_in_list_of_dicts(lists, 'id', 'idList')
            cls.LISTS = change_key_in_list_of_dicts(lists, 'name', 'nameList')

        return cls.LISTS

    @staticmethod
    def get_items():
        cards = requests.get(
            TrelloApi.URL_GET_CARDS, params=TrelloApi.PARAMS_GET_CARDS).json()
        lists = TrelloApi.get_lists()
        items = join_lists_of_dicts(cards, lists, 'idList')
        return items
