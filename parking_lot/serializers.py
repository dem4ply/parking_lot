from marshmallow import Schema, fields, validate


not_blank = validate.Length(min=1, error='Field cannot be blank.')


class Add(Schema):
    car = fields.String(
        required=True, data_key='car', attribute='license_plate',
        allow_none=False, validate=not_blank)
    tariff = fields.String(required=True)


class AddOutput(Schema):
    car = fields.String(required=True, attribute='license_plate')
    tariff = fields.String(required=True)
    status = fields.String(default='success')
    location = fields.Int(required=True)
    start = fields.DateTime("%Y-%m-%d %H:%M:%S")


class Remove(Schema):
    location = fields.Int(required=True)


class RemoveOutput(Schema):
    car = fields.String(required=True, attribute='license_plate')
    tariff = fields.String(required=True)
    status = fields.String(default='success')
    location = fields.Int(required=True)
    start = fields.DateTime("%Y-%m-%d %H:%M:%S")
    finish = fields.DateTime("%Y-%m-%d %H:%M:%S")
    fee = fields.Float()


class ListOutput(Schema):
    cars = fields.Nested(AddOutput, many=True)
    status = fields.String(default='success')
