from todo_app.data.sort_manager import get_current_sort_order, set_current_sort_order, sort
from todo_app.data.FieldNames import FieldNames
from todo_app.data.Item import Item
from todo_app.data.TrelloApi import TrelloApi
from todo_app.utils import to_utc_datetime_object


"""This is a wraper class hiding the underneath Trello API."""


class Items:

    @staticmethod
    def get_items():
        trello_items = TrelloApi.get_items_lists()
        items = []
        for trello_item in trello_items:
            items.append(Item(trello_item[FieldNames.ID], trello_item[FieldNames.NAME],
                              trello_item[FieldNames.STATUS], to_utc_datetime_object(trello_item[FieldNames.DATE_LAST_ACTIVITY])))
        items = sort(items)
        return items

    @staticmethod
    def add_item(item_name):
        return TrelloApi.add_item(item_name)

    @staticmethod
    def delete_item(item_id):
        return TrelloApi.delete_item(item_id)

    @staticmethod
    def doing_item(item_id):
        return TrelloApi.doing_item(item_id)

    @staticmethod
    def done_item(item_id):
        return TrelloApi.done_item(item_id)

    @staticmethod
    def get_current_sort_order():
        return get_current_sort_order()

    @staticmethod
    def set_current_sort_order(sortby):
        set_current_sort_order(sortby)
