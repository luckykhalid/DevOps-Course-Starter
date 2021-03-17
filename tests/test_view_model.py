"""Unit tests for ViewModel.py"""

from datetime import datetime
from todo_app.utils import to_utc_datetime_object
from todo_app.data.Item import Item
from todo_app.ViewModel import ViewModel
import pytest


@pytest.fixture
def view_model() -> ViewModel:
    items = []
    items.append(Item('Id01', 'Item Name 01',
                      'To Do', to_utc_datetime_object('2021-03-16T12:30:01.070Z')))
    items.append(Item('Id02', 'Item Name 02',
                      'Doing', to_utc_datetime_object('2021-03-15T12:30:01.070Z')))
    items.append(Item('Id03', 'Item Name 03',
                      'Done', to_utc_datetime_object('2021-03-14T12:30:01.070Z')))
    return ViewModel(items, None)


def test_items(view_model):
    items = view_model.items
    assert len(items) == 3


def test_items_to_do(view_model):
    items = view_model.items_to_do
    assert len(items) == 1
    assert items[0].status == 'To Do'


def test_items_doing(view_model):
    items = view_model.items_doing
    assert len(items) == 1
    assert items[0].status == 'Doing'


def test_items_done(view_model):
    items = view_model.items_done
    assert len(items) == 1
    assert items[0].status == 'Done'


def test_show_all_done_items(view_model):
    assert view_model.show_all_done_items

    # if 5 or more items then don't show all items
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', to_utc_datetime_object('2021-03-14T12:30:01.070Z')))
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', to_utc_datetime_object('2021-03-14T12:30:01.070Z')))
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', to_utc_datetime_object('2021-03-14T12:30:01.070Z')))
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', to_utc_datetime_object('2021-03-14T12:30:01.070Z')))

    assert not view_model.show_all_done_items


def test_items_done_recent(view_model):
    items = view_model.items_done_recent
    assert len(items) == 0

    # if 5 or more items then don't show all items
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', datetime.now()))
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', datetime.now()))
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', datetime.now()))
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', datetime.now()))
    view_model.items.append(
        Item('Id03', 'Item Name 03', 'Done', datetime.now()))

    items = view_model.items_done_recent
    assert len(items) == 5
