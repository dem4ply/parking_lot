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
    def __init__(
            self, car, tariff, location, hourly_fee, daily_fee,
            start=None, finish=None ):
        self.car = car
        self.tariff = tariff
        self.location = location
        if start is None:
            start = datetime.datetime.now()
        self.start = start
        self.finish = finish

        self.hourly_fee = hourly_fee
        self.daily_fee = daily_fee

    def exit( self ):
        self.finish = datetime.datetime.now()

    @property
    def fee( self ):
        if self.is_free_charge:
            return 0

        if self.is_daily:
            return self.proportional_diff_time * self.daily_fee
        if self.is_hourly:
            return self.proportional_diff_time * self.hourly_fee
        raise NotImplementedError(
            f"the tariff {self.tariff} is not implemented" )

    @property
    def is_free_charge( self ):
        diff_time = self.finish - self.start
        return diff_time.total_seconds() // ( 60 * 15 ) < 1

    @property
    def is_daily( self ):
        return self.tariff == 'daily'

    @property
    def is_hourly( self ):
        return self.tariff == 'hourly'

    @property
    def proportional_diff_time( self ):
        diff_time = self.finish - self.start
        if self.is_hourly:
            return ( diff_time.total_seconds() // 3600 ) + 1
        if self.is_daily:
            return ( diff_time.total_seconds() // 86400 ) + 1


class Parking_lot:
    locations = None
    lot = None

    def __init__( self, amount, hourly_fee=1, daily_fee=20 ):
        self.lot = {}
        self.locations = []
        self.amount_lot = amount
        self.hourly_fee = hourly_fee
        self.daily_fee = daily_fee

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
        result = Car(
            car=car, tariff=tariff, location=location,
            hourly_fee=self.hourly_fee, daily_fee=self.daily_fee )
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
