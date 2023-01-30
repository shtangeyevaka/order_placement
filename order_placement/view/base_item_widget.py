import abc

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from order_placement.model import BaseItem


class BaseItemWidget(QtWidgets.QWidget):

    close_issued = pyqtSignal(object)

    def __init__(self, parent: QtWidgets.QWidget, item: BaseItem):
        super().__init__(parent)
        self._ui = self._get_ui_form()
        self._ui.setupUi(self)

        self._item = item
        self._update_by_item(item)
        self._connect_signals()

        # add label with item name and button for removing at the top
        header_layout = QtWidgets.QHBoxLayout()
        self._ui.verticalLayout.insertLayout(0, header_layout)

        lbl_name = QtWidgets.QLabel(self)
        lbl_name.setText(self.item.NAME.capitalize())
        header_layout.addWidget(lbl_name)

        self._btn_remove = QtWidgets.QPushButton(self)
        self._btn_remove.setText('Remove')
        self._btn_remove.clicked.connect(self._on_btn_remove_clicked)
        header_layout.addWidget(self._btn_remove)

        # add line as boundary at the bottom
        line = QtWidgets.QFrame(self)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self._ui.verticalLayout.addWidget(line)

    @abc.abstractmethod
    def _get_ui_form(self):
        pass

    @property
    def item(self) -> BaseItem:
        return self._item

    @abc.abstractmethod
    def _update_by_item(self, item: BaseItem):
        self._ui.spb_quantity.setMinimum(1)
        self._ui.spb_quantity.setMaximum(item.MAX_QUANTITY)
        self._ui.spb_quantity.setValue(item.quantity)

    def _connect_signals(self):
        self._ui.spb_quantity.editingFinished.connect(self._on_spb_quantity_changed)

    def _on_spb_quantity_changed(self):
        self.item.quantity = self._ui.spb_quantity.value()

    def _on_btn_remove_clicked(self):
        self.close_issued.emit(self)
