#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import random
import unittest
from parking_lot.parking_lot import (
    ParkingLot, FullParkingError, Ticket, CannotFindCarError
)
from tests.factories import (
    CarAdd, CarAddDaily, CarAddHourly,
    CarDailyFree, CarHourlyFree,
    CarDailyFee as Car_daily_factory,
    CarHourlyFee as Car_hourly_factory,
)


class TestCar(unittest.TestCase):
    def test_is_free_of_chage_should_be_true_is_less_15_mins(self):
        car = CarDailyFree.build()
        self.assertEqual(car.fee, 0)

        car = CarHourlyFree.build()
        self.assertEqual(car.fee, 0)

    def test_houtly_tariff_should_be_proportional_after_15min(self):
        car = Car_hourly_factory.build()
        self.assertEqual(
            car.fee, car.proportional_diff_time * car.hourly_fee)

    def test_daily_tariff_should_be_proportional_after_15min(self):
        car = Car_daily_factory.build()
        self.assertEqual(
            car.fee, car.proportional_diff_time * car.hourly_fee)


class TestParkingLot(unittest.TestCase):
    amount = 10

    def setUp(self):
        super().setUp()
        self.parking_lot = ParkingLot(amount=self.amount)

    def test_should_work(self):
        self.assertTrue(self.parking_lot)


class TestParkingLotOther(unittest.TestCase):
    amount = 2

    def setUp(self):
        super().setUp()
        self.parking_lot = ParkingLot(amount=self.amount)

    def test_is_full_should_be_false_if_not_full(self):
        self.assertFalse(self.parking_lot.is_full)

    def test_is_full_should_be_true_when_is_fill(self):
        for amount in range(self.amount):
            self.parking_lot.add(**CarAdd.build())
        self.assertTrue(self.parking_lot.is_full)

    def test_is_empty_should_be_true_if_not_full(self):
        self.assertTrue(self.parking_lot.is_empty)

    def test_is_empty_when_have_any_car_should_return_false(self):
        self.parking_lot.add(**CarAdd.build())
        self.assertFalse(self.parking_lot.is_empty)


class TestParkingLotFindNextAvailableLocation(unittest.TestCase):
    amount = 2

    def setUp(self):
        super().setUp()
        self.parking_lot = ParkingLot(amount=self.amount)
        for amount in range(self.amount):
            self.parking_lot.add(**CarAdd.build())

    def test_when_is_full_should_not_raise_value_exception(self):
        self.assertTrue(self.parking_lot.is_full)
        with self.assertRaises(FullParkingError):
            self.parking_lot.find_next_available_location()


class TestParkingLotAdd(TestParkingLot):

    def setUp(self):
        super().setUp()
        self.new_car = CarAdd.build()

    def test_add_car_should_be_in_the_parking(self):
        self.parking_lot.add(**self.new_car)
        self.assertIn(self.new_car['license_plate'], self.parking_lot)

    def test_add_car_should_add_current_date_and_location(self):
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['license_plate']]
        self.assertIsInstance(car_data, Ticket)
        self.assertIsNotNone(car_data.location)
        self.assertTrue(car_data.start)

    def test_location_should_be_int(self):
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['license_plate']]
        self.assertIsInstance(car_data.location, int)

    def test_start_should_be_datetime(self):
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['license_plate']]
        self.assertIsInstance(car_data.start, datetime.datetime)

    def test_add_car_should_set_start_to_now_date(self):
        now = datetime.datetime.now()
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['license_plate']]
        diff_date = car_data.start - now
        self.assertLessEqual(abs(diff_date.total_seconds()), 1)

    def test_add_car_should_return_the_car_obj(self):
        car_data = self.parking_lot.add(**self.new_car)
        self.assertIsNotNone(car_data)
        self.assertTrue(car_data)

    def test_add_car_when_is_full_should_raise_full_parking(self):
        self.parking_lot.amount_lot = 2
        self.parking_lot.add(**CarAdd.build())
        self.parking_lot.add(**CarAdd.build())
        with self.assertRaises(FullParkingError):
            self.parking_lot.add(**CarAdd.build())


class TestParkingLotRemove(TestParkingLot):

    def setUp(self):
        super().setUp()
        for amount in range(self.amount):
            self.parking_lot.add(**CarAdd.build())

    def test_remove_random_randon_car_from_location_should_work(self):
        location = random.randint(0, self.amount - 1)
        car = self.parking_lot.remove(location)
        self.assertIsNotNone(car)
        self.assertIsInstance(car, Ticket)

    def test_remove_empty_location_should_raise_exception(self):
        self.parking_lot.remove(5)
        with self.assertRaises(CannotFindCarError):
            self.parking_lot.remove(5)

    def test_when_remove_should_no_be_in_the_locations_or_lot(self):
        car = self.parking_lot.remove(5)
        self.assertIsNone(self.parking_lot.locations[5])
        self.assertNotIn(car.license_plate, self.parking_lot.lot)


class TestParkingLotDailyFee(TestParkingLot):
    def setUp(self):
        super().setUp()
        for amount in range(self.amount):
            self.parking_lot.add(**CarAddDaily.build())

    def get_any_car(self):
        car = next(iter(self.parking_lot.lot.values()))
        return car

    def test_less_of_15_min_fee_should_be_0(self):
        car = self.get_any_car()
        now = datetime.datetime.now()
        diff_time = now - car.start
        self.assertLessEqual(diff_time.total_seconds(), 1)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, 0)
        car = self.get_any_car()
        car.start = car.start - datetime.timedelta(minutes=14, seconds=59)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, 0)

    def test_after_15_min_fee_should_be_proportional_to_fee(self):
        car = self.get_any_car()
        car.start = car.start - datetime.timedelta(minutes=15, seconds=1)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, self.parking_lot.daily_fee)

        car = self.get_any_car()
        car.start = car.start - datetime.timedelta(days=1, seconds=1)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, self.parking_lot.daily_fee * 2)


class TestParkingLotHourlyFee(TestParkingLot):
    def setUp(self):
        super().setUp()
        for amount in range(self.amount):
            self.parking_lot.add(**CarAddHourly.build())

    def get_any_car(self):
        car = next(iter(self.parking_lot.lot.values()))
        return car

    def test_less_of_15_min_fee_should_be_0(self):
        car = self.get_any_car()
        now = datetime.datetime.now()
        diff_time = now - car.start
        self.assertLessEqual(diff_time.total_seconds(), 1)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, 0)
        car = self.get_any_car()
        car.start = car.start - datetime.timedelta(minutes=14, seconds=59)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, 0)

    def test_after_15_min_fee_should_be_proportional_to_fee(self):
        car = self.get_any_car()
        car.start = car.start - datetime.timedelta(minutes=15, seconds=1)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, self.parking_lot.hourly_fee)

        car = self.get_any_car()
        car.start = car.start - datetime.timedelta(hours=1, seconds=1)
        car = self.parking_lot.remove(car.location)
        self.assertEqual(car.fee, self.parking_lot.hourly_fee * 2)
