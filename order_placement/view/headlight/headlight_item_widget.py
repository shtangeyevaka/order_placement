from order_placement.model import HeadlightItem

from .headlight_item_widget_ui import Ui_Form
from ..base_item_widget import BaseItemWidget


class HeadlightItemWidget(BaseItemWidget):

    def _get_ui_form(self):
        return Ui_Form()

    def _update_by_item(self, item: HeadlightItem):
        super()._update_by_item(item)
        self._ui.cmb_type.addItems(item.TYPES_RANGE)
        self._ui.cmb_type.setCurrentText(item.item_type)

    def _connect_signals(self):
        self._ui.cmb_type.currentIndexChanged.connect(self._on_cmb_type_changed)
        self._ui.spb_quantity.editingFinished.connect(self._on_spb_quantity_changed)

    def _on_cmb_type_changed(self):
        self.item.item_type = self._ui.cmb_type.currentText()
