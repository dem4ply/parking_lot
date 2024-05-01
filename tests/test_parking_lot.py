#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import random
import unittest
from parking_lot.parking_lot import (
    Parking_lot, Full_parking_error, Car, Cannot_find_car_error
)
from parking_lot.factories import (
    Car_add, Car_add_daily, Car_add_hourly,
    Car_daily_free, Car_hourly_free,
    Car_daily_fee as Car_daily_factory,
    Car_hourly_fee as Car_hourly_factory,
)


class Test_car(unittest.TestCase):
    def test_is_free_of_chage_should_be_true_is_less_15_mins(self):
        car = Car_daily_free.build()
        self.assertEqual(car.fee, 0)

        car = Car_hourly_free.build()
        self.assertEqual(car.fee, 0)

    def test_houtly_tariff_should_be_proportional_after_15min(self):
        car = Car_hourly_factory.build()
        self.assertEqual(
            car.fee, car.proportional_diff_time * car.hourly_fee)

    def test_daily_tariff_should_be_proportional_after_15min(self):
        car = Car_daily_factory.build()
        self.assertEqual(
            car.fee, car.proportional_diff_time * car.hourly_fee)


class Test_Parking_lot(unittest.TestCase):
    amount = 10

    def setUp(self):
        super().setUp()
        self.parking_lot = Parking_lot(amount=self.amount)

    def test_should_work(self):
        self.assertTrue(self.parking_lot)


class Test_Parking_lot_other(unittest.TestCase):
    amount = 2

    def setUp(self):
        super().setUp()
        self.parking_lot = Parking_lot(amount=self.amount)

    def test_is_full_should_be_false_if_not_full(self):
        self.assertFalse(self.parking_lot.is_full)

    def test_is_full_should_be_true_when_is_fill(self):
        for amount in range(self.amount):
            self.parking_lot.add(**Car_add.build())
        self.assertTrue(self.parking_lot.is_full)

    def test_is_empty_should_be_true_if_not_full(self):
        self.assertTrue(self.parking_lot.is_empty)

    def test_is_empty_when_have_any_car_should_return_false(self):
        self.parking_lot.add(**Car_add.build())
        self.assertFalse(self.parking_lot.is_empty)


class Test_Parking_lot_add(Test_Parking_lot):

    def setUp(self):
        super().setUp()
        self.new_car = Car_add.build()

    def test_add_car_should_be_in_the_parking(self):
        self.parking_lot.add(**self.new_car)
        self.assertIn(self.new_car['car'], self.parking_lot)

    def test_add_car_should_add_current_date_and_location(self):
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['car']]
        self.assertIsInstance(car_data, Car)
        self.assertIsNotNone(car_data.location)
        self.assertTrue(car_data.start)

    def test_location_should_be_int(self):
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['car']]
        self.assertIsInstance(car_data.location, int)

    def test_start_should_be_datetime(self):
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['car']]
        self.assertIsInstance(car_data.start, datetime.datetime)

    def test_add_car_should_set_start_to_now_date(self):
        now = datetime.datetime.now()
        self.parking_lot.add(**self.new_car)
        car_data = self.parking_lot[self.new_car['car']]
        diff_date = car_data.start - now
        self.assertLessEqual(abs(diff_date.total_seconds()), 1)

    def test_add_car_should_return_the_car_obj(self):
        car_data = self.parking_lot.add(**self.new_car)
        self.assertIsNotNone(car_data)
        self.assertTrue(car_data)

    def test_add_car_when_is_full_should_raise_full_parking(self):
        self.parking_lot.amount_lot = 2
        self.parking_lot.add(**Car_add.build())
        self.parking_lot.add(**Car_add.build())
        with self.assertRaises(Full_parking_error):
            self.parking_lot.add(**Car_add.build())


class Test_Parking_lot_remove(Test_Parking_lot):

    def setUp(self):
        super().setUp()
        for amount in range(self.amount):
            self.parking_lot.add(**Car_add.build())

    def test_remove_random_randon_car_from_location_should_work(self):
        location = random.randint(0, self.amount - 1)
        car = self.parking_lot.remove(location)
        self.assertIsNotNone(car)
        self.assertIsInstance(car, Car)

    def test_remove_empty_location_should_raise_exception(self):
        self.parking_lot.remove(5)
        with self.assertRaises(Cannot_find_car_error):
            self.parking_lot.remove(5)

    def test_when_remove_should_no_be_in_the_locations_or_lot(self):
        car = self.parking_lot.remove(5)
        self.assertIsNone(self.parking_lot.locations[5])
        self.assertNotIn(car.car, self.parking_lot.lot)


class Test_Parking_lot_daily_fee(Test_Parking_lot):
    def setUp(self):
        super().setUp()
        for amount in range(self.amount):
            self.parking_lot.add(**Car_add_daily.build())

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


class Test_Parking_lot_hourly_fee(Test_Parking_lot):
    def setUp(self):
        super().setUp()
        for amount in range(self.amount):
            self.parking_lot.add(**Car_add_hourly.build())

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
