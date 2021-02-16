import os
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

    TRELLO_BOARD_ID = '60254e45c1345502980ecbf7'
    TRELLO_LIST_TODO_ID = '60254e45c1345502980ecbf8'
    TRELLO_LIST_DONE_ID = '60254e45c1345502980ecbfa'

    TRELLO_URL_GET_CARDS = f'https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/cards?key={TRELLO_KEY}&token={TRELLO_TOKEN}&fields=name,idList'

    @staticmethod
    def get_items():
        response = requests.get(TrelloApi.TRELLO_URL_GET_CARDS)
        return response
