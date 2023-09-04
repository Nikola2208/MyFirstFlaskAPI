from marshmallow import Schema, fields


class ItemInStoreSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)


class TagInStoreSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)


class ItemUpdateSchema(Schema):
    name = fields.String(required=False)
    price = fields.Float(required=False)
    description = fields.String(required=False)


class ItemCreateSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)
    description = fields.String(required=True)


class ItemResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    description = fields.String(required=True)
    store_id = fields.Int(required=True)
    tags = fields.List(fields.Nested(TagInStoreSchema()))


class TagCreateSchema(Schema):
    name = fields.String(required=True)
    store_id = fields.Int(required=True)


class TagResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    store_id = fields.Int(required=True)
    items = fields.List(fields.Nested(ItemInStoreSchema()))


class StoreUpdateSchema(Schema):
    name = fields.String(required=False)


class StoreCreateSchema(Schema):
    name = fields.String(required=True)


class StoreResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    items = fields.List(fields.Nested(ItemInStoreSchema()))
    tags = fields.List(fields.Nested(TagInStoreSchema()))


class UserRequestSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserLoginSchema(UserRequestSchema):
    pass


class UserRegistrationSchema(UserRequestSchema):
    email = fields.String(required=True)
    role = fields.String(required=True)


class UserResponseSchema(Schema):
    id = fields.Int(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
