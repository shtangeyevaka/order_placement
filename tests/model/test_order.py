from unittest import mock

import pytest

from order_placement.model import Order, HeadlightItem, EngineItem


class TestOrder:
    def setup(self):
        self.order = Order()

    def test_add_item(self):
        with mock.patch.object(Order, 'items_changed') as items_changed_mock:
            item = self.order.add_item(HeadlightItem.TITLE)

        items_changed_mock.emit.assert_called_once_with([item], [])

    def test_remove_non_existing_item(self):
        with pytest.raises(ValueError):
            with mock.patch.object(Order, 'items_changed') as items_changed_mock:
                self.order.remove_item(HeadlightItem())

        items_changed_mock.emit.assert_not_called()

    def test_remove_existing_item(self):
        item = self.order.add_item(EngineItem.TITLE)
        with mock.patch.object(Order, 'items_changed') as items_changed_mock:
            self.order.remove_item(item)

        items_changed_mock.emit.assert_called_once_with([], [item])
