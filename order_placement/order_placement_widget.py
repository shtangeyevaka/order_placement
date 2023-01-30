import sys
from typing import Optional, List, Dict

from PyQt5 import QtWidgets

from order_placement.model import BaseItem, HeadlightItem, DoorItem, EngineItem, Order
from order_placement.view import BaseItemWidget, HeadlightItemWidget, DoorItemWidget, EngineItemWidget
from order_placement_widget_ui import Ui_Form


class OrderPlacementWidget(QtWidgets.QWidget):

    ITEMS_WIDGETS = {
        HeadlightItem: HeadlightItemWidget,
        DoorItem: DoorItemWidget,
        EngineItem: EngineItemWidget
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ui = Ui_Form()
        self._ui.setupUi(self)

        self._ui.cmb_items.addItems(item_cls.NAME for item_cls in self.ITEMS_WIDGETS)
        self._ui.btn_open.clicked.connect(self._on_btn_open_clicked)
        self._ui.btn_save.clicked.connect(self._on_btn_save_clicked)
        self._ui.btn_add.clicked.connect(self._on_btn_add_clicked)

        self._order = Order()
        self._order.items_changed.connect(self._on_items_changed)

        self._items_widgets: Dict[BaseItem, BaseItemWidget] = dict()

    def _add_item_widget(self, item: BaseItem) -> Optional[BaseItemWidget]:
        widget_cls = self.ITEMS_WIDGETS.get(type(item))
        if not widget_cls:
            return None

        item_widget = widget_cls(self, item)
        item_widget.close_issued.connect(self._on_item_widget_close_issued)
        self._ui.layout_items.addWidget(item_widget)
        self._items_widgets[item] = item_widget
        return item_widget

    def _remove_item_widget(self, item: BaseItem):
        item_widget = self._items_widgets[item]
        del self._items_widgets[item_widget.item]
        self._ui.layout_items.removeWidget(item_widget)
        item_widget.deleteLater()

    def _on_items_changed(self, removed_items: List[BaseItem], added_items: List[BaseItem]):
        for item in removed_items:
            self._remove_item_widget(item)

        for item in added_items:
            self._add_item_widget(item)

    def _on_item_widget_close_issued(self, item_widget: BaseItemWidget):
        self._order.remove_item(item_widget.item)

    def _on_btn_open_clicked(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose file', filter='*.yml')
        if file_name:
            self._order.load_from_file(file_name)

    def _on_btn_save_clicked(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Choose file', filter='*.yml')
        self._order.save_to_file(file_name)

    def _on_btn_add_clicked(self):
        item_name = self._ui.cmb_items.currentText()
        self._order.add_item(item_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = OrderPlacementWidget()
    widget.show()
    app.exec_()
