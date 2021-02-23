from flask import session
from operator import itemgetter

SORT_ORDER_KEY = 'sort_order'
SORT_ORDER_IS_DESCENDING = 'is_descending'

_DEFAULT_SORT_ORDER_IS_DESCENDING = False
_DEFAULT_SORT_ORDER_KEY = 'name'
_DEFAULT_SORT_ORDER = {SORT_ORDER_KEY: _DEFAULT_SORT_ORDER_KEY,
                       SORT_ORDER_IS_DESCENDING: _DEFAULT_SORT_ORDER_IS_DESCENDING}


def get_current_sort_order():
    return session.get(SORT_ORDER_KEY, _DEFAULT_SORT_ORDER)


def set_current_sort_order(sortby):
    current_sort_order = get_current_sort_order()
    if current_sort_order[SORT_ORDER_KEY] == sortby:
        current_sort_order[SORT_ORDER_IS_DESCENDING] = not current_sort_order[SORT_ORDER_IS_DESCENDING]
    else:
        current_sort_order[SORT_ORDER_IS_DESCENDING] = _DEFAULT_SORT_ORDER_IS_DESCENDING

    current_sort_order[SORT_ORDER_KEY] = sortby
    session[SORT_ORDER_KEY] = current_sort_order
    return get_current_sort_order()


def sort(items):
    current_sort_order = get_current_sort_order()
    items = sorted(items, key=itemgetter(
        current_sort_order[SORT_ORDER_KEY]), reverse=current_sort_order[SORT_ORDER_IS_DESCENDING])
    return items
