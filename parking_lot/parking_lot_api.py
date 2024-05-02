# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restx import Api, Resource
from marshmallow.exceptions import ValidationError

from parking_lot.serializers import (
    Add as AddSerializer,
    AddOutput as AddOutputSerializer,
    Remove as RemoveSerializer,
    RemoveOutput as RemoveOutputSerializer,
    ListOutput as ListOutputSerializer,
)
from parking_lot.parking_lot import ParkingLot, ParkingLotError

parking_lot_db = ParkingLot(amount=10)

app = Flask(__name__)
api = Api(app)


class Add(Resource):
    def get(self):
        serializer = AddSerializer()
        data = serializer.load(request.args)
        car = parking_lot_db.add(**data)
        return AddOutputSerializer().dump(car)


class Remove(Resource):
    def get(self):
        serializer = RemoveSerializer()
        data = serializer.load(request.args)
        car = parking_lot_db.remove(**data)
        return RemoveOutputSerializer().dump(car)


class List(Resource):
    def get(self):
        return ListOutputSerializer().dump(
            {'cars': iter(parking_lot_db)})


def join_messages(messages):
    for k, v in messages.items():
        for msg in v:
            if msg == 'Missing data for required field.':
                yield f"missing {k} data field"
            if msg == 'Field cannot be blank.':
                yield f"field {k} cannot be blank"


@api.errorhandler(ValidationError)
def handler_validation_error(error):
    del error.data
    error_msg = ", ".join(join_messages(error.messages))
    result = {
        'status': 'error',
        'error': f"{error_msg}."
    }
    return result, 400


@api.errorhandler(ParkingLotError)
def handler_parking_error(error):
    return {}, 400


api.add_resource(Add, '/add')
api.add_resource(Remove, '/remove')
api.add_resource(List, '/list')


app.config['ERROR_INCLUDE_MESSAGE'] = False
