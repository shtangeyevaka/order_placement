from typing import Tuple

from PyQt5 import QtWidgets

from order_placement.model import EngineItem, FuelType
from .engine_item_widget_ui import Ui_Form
from ..base_item_widget import BaseItemWidget


class EngineItemWidget(BaseItemWidget):

    def _get_ui_form(self):
        return Ui_Form()

    def _update_by_item(self, item: EngineItem):
        super()._update_by_item(item)

        self._ui.cmb_gas_capacity.addItems(item.CAPACITY_RANGE[FuelType.GAS])
        self._ui.cmb_diesel_capacity.addItems(item.CAPACITY_RANGE[FuelType.DIESEL])

        btn_type, _, _ = self._get_widgets_by_fuel_type(self.item.item_type)
        btn_type.setChecked(True)
        self._on_btn_type_toggled()

    def _connect_signals(self):
        for fuel_type in FuelType:
            btn_type, _, cmb_capacity = self._get_widgets_by_fuel_type(fuel_type)
            btn_type.toggled.connect(self._on_btn_type_toggled)
            cmb_capacity.currentIndexChanged.connect(self._on_cmb_capacity_changed)

    def _on_btn_type_toggled(self):
        selected_type = self._get_selected_type()
        self.item.item_type = selected_type

        for fuel_type in FuelType:
            _, lbl, cmb_capacity = self._get_widgets_by_fuel_type(fuel_type)
            is_enabled = fuel_type == selected_type
            lbl.setEnabled(is_enabled)
            cmb_capacity.setEnabled(is_enabled)

            if is_enabled:
                self.item.capacity = cmb_capacity.currentText()

    def _on_cmb_capacity_changed(self):
        selected_type = self._get_selected_type()
        _, _, cmb_capacity = self._get_widgets_by_fuel_type(selected_type)
        self.item.capacity = cmb_capacity.currentText()

    def _get_selected_type(self) -> FuelType:
        return FuelType.GAS if self._ui.radio_btn_gas.isChecked() else FuelType.DIESEL

    def _get_widgets_by_fuel_type(
            self, fuel_type: FuelType
    ) -> Tuple[QtWidgets.QRadioButton, QtWidgets.QLabel, QtWidgets.QComboBox]:
        if fuel_type == FuelType.GAS:
            return self._ui.radio_btn_gas, self._ui.lbl_gas_capacity, self._ui.cmb_gas_capacity
        else:
            return self._ui.radio_btn_diesel, self._ui.lbl_diesel_capacity, self._ui.cmb_diesel_capacity
