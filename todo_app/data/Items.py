from todo_app.data.sort_manager import get_current_sort_order, set_current_sort_order, sort
from todo_app.data.FieldNames import FieldNames
from todo_app.data.Item import Item
from todo_app.data.MongoDbApi import MongoDbApi


"""This is a wrapper class hiding the underneath MongoDB API."""


class Items:

    @staticmethod
    def get_items():
        db_items = MongoDbApi.get_items()
        items = []
        for db_item in db_items:
            items.append(Item(db_item[FieldNames.ID], db_item[FieldNames.TITLE],
                              db_item[FieldNames.STATUS], db_item[FieldNames.DATE_LAST_ACTIVITY]))
        items = sort(items)
        return items

    @staticmethod
    def add_item(item_title):
        return MongoDbApi.add_item(item_title)

    @staticmethod
    def delete_item(item_id):
        return MongoDbApi.delete_item(item_id)

    @staticmethod
    def doing_item(item_id):
        return MongoDbApi.doing_item(item_id)

    @staticmethod
    def done_item(item_id):
        return MongoDbApi.done_item(item_id)

    @staticmethod
    def get_current_sort_order():
        return get_current_sort_order()

    @staticmethod
    def set_current_sort_order(sortby):
        set_current_sort_order(sortby)
