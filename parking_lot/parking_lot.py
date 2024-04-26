# -*- coding: utf-8 -*-
import datetime

       #{"car": "X774HY98", "tariff": "hourly", "location": 1, "start": "2014-10-01 14:11:45"},

class Parking_lot:
    loot = {}
    amount_lot = 0
    locations = []

    def __init__( self, amount ):
        self.amount_lot = amount
        self.loot = {}
        self.locations = []

    def add( self, car, tariff ):
        location = self.find_next_available_location()
        start = datetime.datetime.now()
        self.loot[ car ] = {
            'car': car,
            'tariff': tariff,
            'location': location,
            'start': start,
        }

    def find_next_available_location( self ):
        return len( self.locations ) + 1

    def __contains__( self, index ):
        return index in self.loot

    def __getitem__( self, index ):
        return self.loot[ index ]
