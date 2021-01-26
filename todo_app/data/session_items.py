from flask import session
from operator import itemgetter

STATUS_NOT_STARTED = 'Not Started'

_DEFAULT_ITEMS = [
    {'id': 1, 'status': STATUS_NOT_STARTED, 'title': 'List saved todo items'},
    {'id': 2, 'status': STATUS_NOT_STARTED, 'title': 'Allow new items to be added'}
]

_DEFAULT_SORT_ORDER = {'column': 'id', 'descending': False}


def get_current_sort_order():
    return session.get('sortorder', _DEFAULT_SORT_ORDER)

def set_current_sort_order(sortby):
    current_sort_order = get_current_sort_order()
    if current_sort_order['column'] == sortby:
        current_sort_order['descending'] = not current_sort_order['descending']
    else:
        current_sort_order['descending'] = False

    current_sort_order['column'] = sortby
    session['sortorder'] = current_sort_order
    return get_current_sort_order()


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    items = session.get('items', _DEFAULT_ITEMS)
    current_sort_order = get_current_sort_order()
    items = sorted(items, key=itemgetter(current_sort_order['column']),
                   reverse=current_sort_order['descending'])
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


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    item_id = items[-1]['id'] + 1 if items else 0

    item = {'id': item_id, 'title': title, 'status': 'Not Started'}

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
