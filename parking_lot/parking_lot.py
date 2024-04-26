# -*- coding: utf-8 -*-
import datetime


class Parking_lot_error( Exception ):
    message = 'unhandle error with parking lot'

    def __init__( self, message=None ):
        if message is None:
            message = self.message
        self.data = {
            'status': 'error',
            'error': message
        }


class Full_parking_error( Parking_lot_error ):
    message = 'No free space.'


class Cannot_find_car_error( Parking_lot_error ):
    message = 'Cannot find a car in the location {}.'

    def __init__( self, location=None ):
        message = self.message.format( location )
        self.data = {
            'status': 'error',
            'error': message
        }


class Car:
    def __init__( self, car, tariff, location, fee=0 ):
        self.car = car
        self.tariff = tariff
        self.location = location
        self.fee = fee
        self.start = datetime.datetime.now()
        self.finish = None

    def exit( self ):
        self.finish = datetime.datetime.now()


class Parking_lot:
    locations = None
    lot = None

    def __init__( self, amount ):
        self.lot = {}
        self.locations = []
        self.amount_lot = amount

    @property
    def amount_lot( self ):
        return self._amount_lot

    @amount_lot.setter
    def amount_lot( self, value ):
        self._amount_lot = value
        self.locations = [ None ] * self._amount_lot
        for v in self.lot.values():
            self.locations[ v.location ] = v

    def add( self, car, tariff ):
        if self.is_full:
            raise Full_parking_error

        location = self.find_next_available_location()
        result = Car( car=car, tariff=tariff, location=location, )
        self.locations[ location ] = result
        self.lot[ car ] = result
        return result

    def remove( self, location ):
        car = self.locations[ location ]
        if car is None:
            raise Cannot_find_car_error( location )
        self.locations[ location ] = None
        del self.lot[ car.car ]
        car.exit()
        return car

    @property
    def is_full( self ):
        return (
            sum( ( 1 for i in self.locations if i is not None ) )
            == self.amount_lot )
        return len( self.lot ) >= self.amount_lot

    @property
    def is_empty( self ):
        return (
            sum( ( 1 for i in self.locations if i is None ) )
            == self.amount_lot )

    def find_next_available_location( self ):
        return self.locations.index( None )

    def __contains__( self, index ):
        return index in self.lot

    def __getitem__( self, index ):
        return self.lot[ index ]

    def __iter__( self ):
        return iter( self.lot.values() )
