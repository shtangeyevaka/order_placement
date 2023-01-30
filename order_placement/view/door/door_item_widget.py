from order_placement.model import DoorItem
from .door_item_widget_ui import Ui_Form
from ..base_item_widget import BaseItemWidget


class DoorItemWidget(BaseItemWidget):

    def _get_ui_form(self):
        return Ui_Form()

    def _update_by_item(self, item: DoorItem):
        super()._update_by_item(item)

        self._ui.cmb_vert_type.addItems(item.VER_TYPES_RANGE)
        self._ui.cmb_hor_type.addItems(item.HOR_TYPES_RANGE)
        self._ui.cmb_vert_type.setCurrentText(self.item.item_type[1])
        self._ui.cmb_hor_type.setCurrentText(self.item.item_type[0])

    def _connect_signals(self):
        super()._connect_signals()
        self._ui.cmb_vert_type.currentIndexChanged.connect(self._on_cmb_type_changed)
        self._ui.cmb_hor_type.currentIndexChanged.connect(self._on_cmb_type_changed)

    def _on_cmb_type_changed(self):
        self.item.item_type = [self._ui.cmb_hor_type.currentText(), self._ui.cmb_vert_type.currentText()]
