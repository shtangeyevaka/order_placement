from marshmallow import fields, validate, Schema, post_load, ValidationError, pre_dump, validates_schema
from marshmallow_oneofschema import OneOfSchema

from order_placement.model import HeadlightItem, DoorItem, EngineItem, Order


class HeadlightSchema(Schema):
    qty = fields.Integer(required=True, validate=validate.Range(min=1, max=None), attribute='quantity')
    type = fields.String(required=True, validate=validate.OneOf(HeadlightItem.TYPES_RANGE), attribute='item_type')

    @post_load
    def make_headlight_item(self, data, **kwargs) -> HeadlightItem:
        return HeadlightItem(**data)


class DoorSchema(Schema):
    qty = fields.Integer(required=True, attribute='quantity')
    type = fields.Tuple(
        [fields.String(validate=validate.OneOf(DoorItem.HOR_TYPES_RANGE)),
         fields.String(validate=validate.OneOf(DoorItem.VER_TYPES_RANGE)), ],
        attribute='item_type'
    )

    @post_load
    def make_door_item(self, data, **kwargs) -> DoorItem:
        return DoorItem(**data)


class EngineSchema(Schema):
    qty = fields.Integer(required=True, attribute='quantity')
    type = fields.String(required=True, validate=validate.OneOf(EngineItem.TYPES_RANGE), attribute='item_type')
    capacity = fields.String(required=True)

    @validates_schema
    def validate_capacity(self, data, **kwargs):
        item_type = data['item_type']

        if data['capacity'] not in EngineItem.CAPACITY_RANGE[item_type]:
            raise ValidationError('Invalid capacity range!')

    @post_load
    def make_engine_item(self, data, **kwargs) -> EngineItem:
        return EngineItem(**data)


class OneOfItemsSchema(OneOfSchema):
    type_schemas = {HeadlightItem.TITLE: HeadlightSchema, DoorItem.TITLE: DoorSchema, EngineItem.TITLE: EngineSchema}
    type_field = 'item'

    def get_obj_type(self, obj) -> str:
        if type(obj) in (HeadlightItem, DoorItem, EngineItem):
            return obj.TITLE

        raise NotImplementedError()


class OrderSchema(Schema):
    order = fields.Nested(OneOfItemsSchema, many=True)

    @post_load
    def make_order(self, data, **kwargs):
        order_model = Order()
        order_model._items = data['order']
        return order_model

    @pre_dump
    def make_dict(self, order_model, **kwargs):
        return {'order': order_model.items}
