import enum


class BaseItem:

    NAME = ''
    MAX_QUANTITY = 100

    def __init__(self):
        self._props = dict()
        self._register_prop('quantity', lambda x: x is not None and 1 <= x <= self.MAX_QUANTITY)
        self.quantity = 1
        self.item_type = ''

    def _register_prop(self, name: str, validate_func):
        self._props[name] = validate_func

    # def __setattr__(self, key, value):
    #     if not hasattr(self, '_props') or key not in self._props:
    #         return super().__setattr__(key, value)
    #
    #     validate_func = self._props[key]
    #     if validate_func(value):
    #         return super().__setattr__(key, value)
    #     else:
    #         raise ValueError(f'Incorrect value = {value} for {key}!')

    def from_dict(self, d: dict):
        self.item_type = d.get('type')
        self.quantity = d.get('qty')

    def to_dict(self) -> dict:
        return {'item': self.NAME, 'type': self.item_type, 'qty': self.quantity}


class HeadlightItem(BaseItem):

    NAME = 'headlight'
    TYPES_RANGE = ['left', 'right']

    def __init__(self):
        super().__init__()
        self._register_prop('item_type', lambda x: x in self.TYPES_RANGE)
        self.item_type = 'left'


class DoorItem(BaseItem):

    NAME = 'door'
    HOR_TYPES_RANGE = ['left', 'right']
    VER_TYPES_RANGE = ['front', 'back']

    def __init__(self):
        super().__init__()
        self._register_prop('item_type', lambda x: x[0] in self.HOR_TYPES_RANGE and x[1] in self.VER_TYPES_RANGE)
        self.item_type = ['left', 'front']


class FuelType(enum.Enum):
    GAS = 'gas'
    DIESEL = 'diesel'


class EngineItem(BaseItem):

    NAME = 'engine'
    TYPES_RANGE = [FuelType.GAS, FuelType.DIESEL]
    CAPACITY_RANGE = {
        FuelType.GAS: ['1.4', '1.6', '1.8'],
        FuelType.DIESEL: ['1.2', '1.4', '1.6']
    }

    def __init__(self):
        super().__init__()

        self._register_prop('item_type', lambda x: x in self.TYPES_RANGE)
        self.item_type = FuelType.GAS

        self._register_prop('capacity', lambda x: x in self.CAPACITY_RANGE[self.item_type])
        self.capacity = self.CAPACITY_RANGE[self.item_type][0]

    def from_dict(self, d: dict):
        super().from_dict(d)
        self.capacity = d.get('capacity')
        self.item_type = FuelType.GAS if d['type'] == 'gas' else FuelType.DIESEL

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['type'] = self.item_type.value
        d['capacity'] = self.capacity
        return d
