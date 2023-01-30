import enum
from typing import Optional


class BaseItem:
    TITLE = ''
    _DEFAULT_TYPE = None

    def __init__(self, item_type: Optional[str] = None, quantity: int = 1):
        self.quantity = quantity
        self.item_type = item_type if item_type is not None else self._DEFAULT_TYPE


class HeadlightItem(BaseItem):
    TITLE = 'headlight'
    TYPES_RANGE = ['left', 'right']
    _DEFAULT_TYPE = TYPES_RANGE[0]


class DoorItem(BaseItem):
    TITLE = 'door'
    HOR_TYPES_RANGE = ['left', 'right']
    VER_TYPES_RANGE = ['front', 'back']
    _DEFAULT_TYPE = [HOR_TYPES_RANGE[0], VER_TYPES_RANGE[0]]


class FuelType(enum.StrEnum):
    GAS = 'gas'
    DIESEL = 'diesel'


class EngineItem(BaseItem):
    TITLE = 'engine'
    TYPES_RANGE = [FuelType.GAS, FuelType.DIESEL]
    CAPACITY_RANGE = {
        FuelType.GAS: ['1.4', '1.6', '1.8'],
        FuelType.DIESEL: ['1.2', '1.4', '1.6']
    }
    _DEFAULT_TYPE = TYPES_RANGE[0]

    def __init__(self, item_type: Optional[FuelType] = None, capacity: Optional[str] = None, quantity: int = 1):
        super().__init__(item_type, quantity)
        self.capacity = capacity if capacity is not None else self.CAPACITY_RANGE[self.item_type]
