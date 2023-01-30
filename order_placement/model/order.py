from typing import List, Optional

import yaml
from PyQt5 import QtCore
from marshmallow import ValidationError

from .items import HeadlightItem, DoorItem, EngineItem, BaseItem


class InvalidOrderFileException(Exception):
    def __init__(self):
        super().__init__('Invalid file format')


class Order(QtCore.QObject):

    items_changed = QtCore.pyqtSignal(list, list)
    _ITEMS_RANGE = dict((item.TITLE, item) for item in (HeadlightItem, DoorItem, EngineItem))

    def __init__(self):
        super().__init__()
        self._items: List[BaseItem] = []

    def add_item(self, name: str) -> Optional[BaseItem]:
        item = self._add_item_impl(name)
        if item:
            self.items_changed.emit([item], [])

        return item

    def _add_item_impl(self, name: str) -> BaseItem:
        item_cls = self._ITEMS_RANGE[name]
        item = item_cls()
        self._items.append(item)
        return item

    def remove_item(self, item: BaseItem):
        self._remove_item_impl(item)
        self.items_changed.emit([], [item])

    def _remove_item_impl(self, item: BaseItem):
        self._items.remove(item)

    @property
    def items(self) -> List[BaseItem]:
        return self._items

    def load_from_file(self, file_name: str):
        with open(file_name) as f:
            order_schema = self._get_schema()
            try:
                data = yaml.full_load(f)
                loaded_order_model = order_schema.load(data)
                new_items = loaded_order_model.items
            except (ValidationError, yaml.YAMLError) as exc:
                raise InvalidOrderFileException() from exc

        # remove old items and save new items
        removed_items = self._items.copy()
        for item in removed_items:
            self._remove_item_impl(item)

        self._items = new_items
        self.items_changed.emit(self._items, removed_items)

    def save_to_file(self, file_name: str):
        schema = self._get_schema()
        data = schema.dump(self)
        with open(file_name, 'w') as f:
            yaml.dump(data, f, yaml.Dumper, sort_keys=False)

    @staticmethod
    def _get_schema():
        from order_placement.serializers import OrderSchema
        return OrderSchema()
