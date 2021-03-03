from todo_app.data.sort_manager import sort
from todo_app.data.FieldNames import FieldNames
from todo_app.data.Item import Item
from todo_app.data.TrelloApi import TrelloApi


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
