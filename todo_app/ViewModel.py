from todo_app.data.FieldNames import FieldNames
from todo_app.data.Status import Status
from flask import session


class ViewModel:
    def __init__(self, items, sort_order):
        self._items = items
        self._sort_order = sort_order
        self._show_all_done_items = False

    @property
    def items(self):
        return self._items

    @property
    def items_to_do(self):
        return [item for item in self._items if item.status == Status.TODO.value]

    @property
    def items_doing(self):
        return [item for item in self._items if item.status == Status.DOING.value]

    @property
    def items_done(self):
        return [item for item in self._items if item.status == Status.DONE.value]

    @property
    def sort_order(self):
        return self._sort_order

    @property
    def active_tab(self):
        return session.get(FieldNames.ACTIVE_TAB, Status.TODO.value)

    @active_tab.setter
    def active_tab(self, active_tab):
        session[FieldNames.ACTIVE_TAB] = active_tab

    @property
    def show_all_done_items(self):
        return self._show_all_done_items
