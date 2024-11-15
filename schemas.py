from marshmallow import Schema, ValidationError, fields


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Required field(s) not provided.")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=must_not_be_blank)
    is_admin = fields.Bool()


class PropertySchema(Schema):
    id = fields.Int(dump_only=True)
    address = fields.Str(required=True, validate=must_not_be_blank)
    postcode = fields.Str(required=True, validate=must_not_be_blank)
    city = fields.Str(required=True, validate=must_not_be_blank)
    number_of_rooms = fields.Int(required=True, validate=must_not_be_blank)
    user_id = fields.Int()
