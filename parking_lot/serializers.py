from marshmallow import Schema, fields


class Add( Schema ):
    car = fields.String( required=True )
    tariff = fields.String( required=True )


class Add_output( Schema ):
    car = fields.String( required=True )
    tariff = fields.String( required=True )
    status = fields.String( default='success' )
    location = fields.Int( required=True )
    start = fields.DateTime( "%Y-%m-%d %H:%M:%S" )


class Remove( Schema ):
    location = fields.Int( required=True )


class Remove_output( Schema ):
    car = fields.String( required=True )
    tariff = fields.String( required=True )
    status = fields.String( default='success' )
    location = fields.Int( required=True )
    start = fields.DateTime( "%Y-%m-%d %H:%M:%S" )
    finish = fields.DateTime( "%Y-%m-%d %H:%M:%S" )
    fee = fields.Float()


class List_output( Schema ):
    cars = fields.Nested( Add_output, many=True )
    status = fields.String( default='success' )
