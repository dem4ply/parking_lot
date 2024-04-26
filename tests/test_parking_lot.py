#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import unittest
from parking_lot.parking_lot import Parking_lot
from parking_lot.factories import car_add

class Test_Parking_lot( unittest.TestCase ):
    amount = 10

    def setUp(self):
        super().setUp()
        self.parking_lot = Parking_lot( amount=self.amount )

    def test_should_work( self ):
        self.assertTrue( self.parking_lot )


class Test_Parking_lot_add( Test_Parking_lot ):

    def setUp(self):
        super().setUp()
        self.new_car = car_add.build()

    def test_add_car_should_be_in_the_parking( self ):
        self.parking_lot.add( **self.new_car )
        self.assertIn( self.new_car[ 'car' ], self.parking_lot )

    def test_add_car_should_add_current_date_and_location( self ):
        self.parking_lot.add( **self.new_car )
        car_data = self.parking_lot[ self.new_car[ 'car' ] ]
        self.assertIn( 'location', car_data )
        self.assertIn( 'start', car_data )
        self.assertTrue( car_data[ 'location' ] )
        self.assertTrue( car_data[ 'start' ] )

    def test_location_should_be_int( self ):
        self.parking_lot.add( **self.new_car )
        car_data = self.parking_lot[ self.new_car[ 'car' ] ]
        self.assertIsInstance( car_data[ 'location' ], int )

    def test_start_should_be_datetime( self ):
        self.parking_lot.add( **self.new_car )
        car_data = self.parking_lot[ self.new_car[ 'car' ] ]
        self.assertIsInstance( car_data[ 'start' ], datetime.datetime )

    def test_add_car_should_set_start_to_now_date( self ):
        now = datetime.datetime.now()
        self.parking_lot.add( **self.new_car )
        car_data = self.parking_lot[ self.new_car[ 'car' ] ]
        diff_date = car_data[ 'start' ] - now
        self.assertLessEqual( abs( diff_date.total_seconds() ), 1 )
