class ViewModel:
    def __init__(self, items, sort_order):
        self._items = items
        self._sort_order = sort_order

    @property
    def items(self):
        return self._items

    @property
    def sort_order(self):
        return self._sort_order
