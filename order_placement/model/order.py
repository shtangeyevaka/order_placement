from typing import List, Optional

import yaml
from PyQt5 import QtCore

from .items import HeadlightItem, DoorItem, EngineItem, BaseItem


class Order(QtCore.QObject):

    FILE_DATA_CAPTION = 'order'
    ITEMS_RANGE = [HeadlightItem, DoorItem, EngineItem]

    items_changed = QtCore.pyqtSignal(list, list)

    def __init__(self):
        super().__init__()
        self._items: List[BaseItem] = []

    def add_item(self, name: str) -> Optional[BaseItem]:
        item = self._add_item_impl(name)
        if item:
            self.items_changed.emit([item], [])

        return item

    def _add_item_impl(self, name: str) -> BaseItem:
        item = None
        for item_cls in self.ITEMS_RANGE:
            if item_cls.NAME == name:
                item = item_cls()
                continue

        if not item:
            return item

        self._items.append(item)
        return item

    def remove_item(self, item: BaseItem):
        self._remove_item_impl(item)
        self.items_changed.emit([], [item])

    def _remove_item_impl(self, item: BaseItem):
        self._items.remove(item)

    def load_from_file(self, file_name: str):
        removed_items = self._items.copy()
        for item in removed_items:
            self._remove_item_impl(item)

        with open(file_name) as f:
            data = yaml.full_load(f)

        items_settings = data.get(self.FILE_DATA_CAPTION) if data else None
        if not items_settings:
            return

        items = []

        for settings in items_settings:
            item = self._add_item_impl(settings.get('item'))
            if not item:
                return

            # try:
            item.from_dict(settings)
            items.append(item)
            # except ValueError:
            #     return

        self._items = items
        self.items_changed.emit(removed_items, self._items)

    def save_to_file(self, file_name: str):
        data = {self.FILE_DATA_CAPTION: [item.to_dict() for item in self._items]}
        with open(file_name, 'w') as f:
            yaml.dump(data, f, yaml.Dumper, sort_keys=False)

    @property
    def items(self) -> List[BaseItem]:
        return self._items
