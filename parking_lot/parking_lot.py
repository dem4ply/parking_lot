# -*- coding: utf-8 -*-
import functools
import datetime
from .tariff import Tariff
from .exceptions import (
    FullParkingError, CarIsInParkingLotError, CannotFindCarError
)


class Ticket:
    def __init__(
            self, license_plate, tariff, location, start=None, finish=None):
        self.license_plate = license_plate
        if isinstance(tariff, str):
            tariff = Tariff.resolve(tariff)
        else:
            tariff = tariff
        self.tariff = tariff
        self.location = location
        if start is None:
            start = datetime.datetime.now()
        self.start = start
        self.finish = finish

    def exit(self):
        self.finish = datetime.datetime.now()

    @property
    def fee(self):
        return self.tariff.fee(self.diff_time)

    @functools.cached_property
    def diff_time(self):
        return self.finish - self.start

    @property
    def proportional_diff_time(self):
        return self.tariff.proportional_diff_time(self.diff_time)

    @property
    def fee_cost(self):
        return self.tariff.fee_cost


class ParkingLot:
    def __init__(self, amount, hourly_fee=1, daily_fee=20):
        self.lot = {}
        self.amount_lot = amount
        self.hourly_fee = hourly_fee
        self.daily_fee = daily_fee

    @property
    def amount_lot(self):
        return self._amount_lot

    @amount_lot.setter
    def amount_lot(self, value):
        self._amount_lot = value
        self._clear_locations()
        for v in self.lot.values():
            self.locations[v.location] = v

    def add(self, license_plate, tariff):
        if self.is_full:
            raise FullParkingError
        if license_plate in self:
            raise CarIsInParkingLotError(license_plate)

        location = self.find_next_available_location()
        result = Ticket(
            license_plate=license_plate, tariff=tariff, location=location,)
        self.locations[location] = result
        self.lot[license_plate] = result
        return result

    def remove(self, location):
        car = self.locations[location]
        if car is None:
            raise CannotFindCarError(location)
        self.locations[location] = None
        del self.lot[car.license_plate]
        car.exit()
        return car

    @property
    def is_full(self):
        return len(self.lot) == self.amount_lot

    @property
    def is_empty(self):
        return not len(self.lot)

    def find_next_available_location(self):
        try:
            return self.locations.index(None)
        except ValueError:
            raise FullParkingError from ValueError

    def clear(self):
        self.lot = {}
        self._clear_locations()

    def _clear_locations(self):
        self.locations = [None] * self.amount_lot

    def __contains__(self, index):
        return index in self.lot

    def __getitem__(self, index):
        return self.lot[index]

    def __iter__(self):
        return iter(self.lot.values())
