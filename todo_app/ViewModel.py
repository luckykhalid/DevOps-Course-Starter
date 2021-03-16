from todo_app.data.Status import Status


class ViewModel:
    def __init__(self, items, sort_order):
        self._items = items
        self._sort_order = sort_order

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
