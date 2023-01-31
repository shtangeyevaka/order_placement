from unittest import mock

import pytest

from order_placement.model import Order, HeadlightItem, EngineItem


@pytest.fixture()
def order_model():
    return Order()


def test_add_item(order_model):
    with mock.patch.object(Order, 'items_changed') as items_changed_mock:
        item = order_model.add_item(HeadlightItem.TITLE)

    items_changed_mock.emit.assert_called_once_with([item], [])


def test_remove_non_existing_item(order_model):
    with pytest.raises(ValueError):
        with mock.patch.object(Order, 'items_changed') as items_changed_mock:
            order_model.remove_item(HeadlightItem())

    items_changed_mock.emit.assert_not_called()


def test_remove_existing_item(order_model):
    item = order_model.add_item(EngineItem.TITLE)
    with mock.patch.object(Order, 'items_changed') as items_changed_mock:
        order_model.remove_item(item)

    items_changed_mock.emit.assert_called_once_with([], [item])
