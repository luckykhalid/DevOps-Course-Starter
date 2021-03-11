from todo_app.data.sort_manager import get_current_sort_order, set_current_sort_order, sort
from todo_app.data.FieldNames import FieldNames
from todo_app.data.Item import Item
from todo_app.data.TrelloApi import TrelloApi


"""This class represents Items wrapper hiding underneath API. UI always calls this class rather than direct interacting with backend API."""


class Items:

    @staticmethod
    def get_items():
        trello_items = TrelloApi.get_items_lists()
        items = []
        for trello_item in trello_items:
            items.append(
                Item(trello_item[FieldNames.FIELD_NAME_ID], trello_item[FieldNames.FIELD_NAME_NAME], trello_item[FieldNames.FIELD_NAME_STATUS]))
        items = sort(items)
        return items

    @staticmethod
    def add_item(item_name):
        return TrelloApi.add_item(item_name)

    @staticmethod
    def delete_item(item_id):
        return TrelloApi.delete_item(item_id)

    @staticmethod
    def start_item(item_id):
        return TrelloApi.start_item(item_id)

    @staticmethod
    def done_item(item_id):
        return TrelloApi.done_item(item_id)

    @staticmethod
    def get_current_sort_order():
        return get_current_sort_order()

    @staticmethod
    def set_current_sort_order(sortby):
        set_current_sort_order(sortby)
