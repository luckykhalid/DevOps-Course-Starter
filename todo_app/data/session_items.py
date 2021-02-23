from todo_app.data.trello_api import TrelloApi
from flask import session
from operator import itemgetter

STATUS_NOT_STARTED = 'Not Started'
SORT_ORDER_KEY = 'sortorderfield'
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


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """

    items = TrelloApi.get_items_lists()
    current_sort_order = get_current_sort_order()
    items = sorted(items, key=itemgetter(
        current_sort_order[SORT_ORDER_KEY]), reverse=current_sort_order[SORT_ORDER_IS_DESCENDING])
    return items


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(name):
    """
    Adds a new item with the specified name to the session.

    Args:
        name: The name of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    item_id = items[-1]['id'] + 1 if items else 0

    item = {'id': item_id, 'name': name, 'status': 'Not Started'}

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id']
                     else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item


def delete_item(id):
    """
    Deletes the item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        Noting is returned
    """
    item = get_item(id)

    # Remove item from the list if exists
    if item != None:
        items = get_items()
        items.remove(item)
        session['items'] = items
