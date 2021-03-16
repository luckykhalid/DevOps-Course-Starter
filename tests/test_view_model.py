"""Unit tests for ViewModel.py"""

from todo_app.data.Item import Item
from todo_app.ViewModel import ViewModel
import pytest


@pytest.fixture
def view_model() -> ViewModel:
    items = []
    items.append(Item('Id01', 'Item Name 01', 'To Do'))
    items.append(Item('Id02', 'Item Name 02', 'Doing'))
    items.append(Item('Id03', 'Item Name 03', 'Done'))
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
