# -*- coding: utf-8 -*-
import functools
import datetime


class ParkingLotError(Exception):
    message = 'unhandle error with parking lot'

    def __init__(self, message=None):
        if message is None:
            message = self.message
        self.data = {
            'status': 'error',
            'error': message
        }


class FullParkingError(ParkingLotError):
    message = 'No free space.'


class CannotFindCarError(ParkingLotError):
    message = 'Cannot find a car in the location {}.'

    def __init__(self, location=None):
        message = self.message.format(location)
        super().__init__(message=message)


class Ticket:
    def __init__(
            self, license_plate, tariff, location, hourly_fee, daily_fee,
            start=None, finish=None):
        self.license_plate = license_plate
        self.tariff = tariff
        self.location = location
        if start is None:
            start = datetime.datetime.now()
        self.start = start
        self.finish = finish

        self.hourly_fee = hourly_fee
        self.daily_fee = daily_fee

    def exit(self):
        self.finish = datetime.datetime.now()

    @property
    def fee(self):
        if self.is_free_charge:
            return 0

        if self.is_daily:
            return self.proportional_diff_time * self.daily_fee
        if self.is_hourly:
            return self.proportional_diff_time * self.hourly_fee
        raise NotImplementedError(
            f"the tariff {self.tariff} is not implemented")

    @functools.cached_property
    def diff_time(self):
        return self.finish - self.start

    @property
    def is_free_charge(self):
        return self.diff_time.total_seconds() // (60 * 15) < 1

    @property
    def is_daily(self):
        return self.tariff == 'daily'

    @property
    def is_hourly(self):
        return self.tariff == 'hourly'

    @property
    def proportional_diff_time(self):
        if self.is_hourly:
            return (self.diff_time.total_seconds() // 3600) + 1
        if self.is_daily:
            return (self.diff_time.total_seconds() // 86400) + 1


class ParkingLot:
    locations = None
    lot = None

    def __init__(self, amount, hourly_fee=1, daily_fee=20):
        self.lot = {}
        self.locations = []
        self.amount_lot = amount
        self.hourly_fee = hourly_fee
        self.daily_fee = daily_fee

    @property
    def amount_lot(self):
        return self._amount_lot

    @amount_lot.setter
    def amount_lot(self, value):
        self._amount_lot = value
        self.locations = [None] * self._amount_lot
        for v in self.lot.values():
            self.locations[v.location] = v

    def add(self, license_plate, tariff):
        if self.is_full:
            raise FullParkingError

        location = self.find_next_available_location()
        result = Ticket(
            license_plate=license_plate, tariff=tariff, location=location,
            hourly_fee=self.hourly_fee, daily_fee=self.daily_fee)
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

    def __contains__(self, index):
        return index in self.lot

    def __getitem__(self, index):
        return self.lot[index]

    def __iter__(self):
        return iter(self.lot.values())
