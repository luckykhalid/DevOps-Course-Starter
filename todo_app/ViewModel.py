from datetime import datetime
from todo_app.utils import to_utc_datetime_object
from todo_app.data.Status import Status


class ViewModel:
    def __init__(self, items, sort_order):
        self._items = items
        self._sort_order = sort_order
        self._active_tab = Status.DONE.value

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
    def items_done_recent(self):
        return [item for item in self.items_done if item.date_last_activity.date() == datetime.today().date()]

    @property
    def sort_order(self):
        return self._sort_order

    @property
    def active_tab(self):
        return self._active_tab

    def is_active_tab(self, tab):
        return (tab == self._active_tab)

    def get_active_tab_class(self, tab):
        if (self.is_active_tab(tab)):
            return ' active'
        return ''

    def get_active_tab_content_class(self, tab):
        if (self.is_active_tab(tab)):
            return ' show active'
        return ''

    @property
    def show_all_done_items(self):
        return len(self.items_done) < 5
