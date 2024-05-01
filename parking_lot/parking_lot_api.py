# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restx import Api, Resource
from marshmallow.exceptions import ValidationError

from parking_lot.serializers import (
    Add as Add_serializer,
    Add_output as Add_output_serializer,
    Remove as Remove_serializer,
    Remove_output as Remove_output_serializer,
    List_output as List_output_serializer,
)
from parking_lot.parking_lot import Parking_lot, Parking_lot_error

parking_lot_db = Parking_lot(amount=10)

app = Flask(__name__)
api = Api(app)


class Add(Resource):
    def get(self):
        serializer = Add_serializer()
        data = serializer.load(request.args)
        car = parking_lot_db.add(**data)
        return Add_output_serializer().dump(car)


class Remove(Resource):
    def get(self):
        serializer = Remove_serializer()
        data = serializer.load(request.args)
        car = parking_lot_db.remove(**data)
        return Remove_output_serializer().dump(car)


class List(Resource):
    def get(self):
        return List_output_serializer().dump(
            {'cars': iter(parking_lot_db)})


def join_messages(messages):
    for k, v in messages.items():
        for msg in v:
            if msg == 'Missing data for required field.':
                yield f"missing {k} data field"


@api.errorhandler(ValidationError)
def handler_validation_error(error):
    del error.data
    error_msg = ", ".join(join_messages(error.messages))
    result = {
        'status': 'error',
        'error': f"{error_msg}."
    }
    return result, 400


@api.errorhandler(Parking_lot_error)
def handler_parking_error(error):
    return {}, 400


api.add_resource(Add, '/add')
api.add_resource(Remove, '/remove')
api.add_resource(List, '/list')


app.config['ERROR_INCLUDE_MESSAGE'] = False
