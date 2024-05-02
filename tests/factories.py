import factory
from factory import fuzzy
from parking_lot.parking_lot import Ticket as CarModel


tariffs = ['hourly', 'daily']


class Car(factory.Factory):
    license_plate = factory.Faker('license_plate')
    tariff = fuzzy.FuzzyChoice(tariffs)
    location = factory.Faker('pyint')
    hourly_fee = factory.Faker('pyint')
    daily_fee = factory.Faker('pyint')

    class Meta:
        model = CarModel


class CarDailyFee(Car):
    tariff = 'hourly'
    start = factory.Faker(
        'date_time_between', start_date='-15d', end_date='-1d')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class CarDailyFree(CarDailyFee):
    start = factory.Faker(
        'date_time_between', start_date='-15m', end_date='now')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class CarHourlyFee(Car):
    tariff = 'hourly'
    start = factory.Faker(
        'date_time_between', start_date='-15h', end_date='-1h')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class CarHourlyFree(CarHourlyFee):
    start = factory.Faker(
        'date_time_between', start_date='-15m', end_date='now')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class CarAdd(factory.Factory):
    license_plate = factory.Faker('license_plate')
    tariff = fuzzy.FuzzyChoice(tariffs)

    class Meta:
        model = dict


class CarAddHourly(factory.Factory):
    license_plate = factory.Faker('license_plate')
    tariff = 'hourly'

    class Meta:
        model = dict


class CarAddDaily(factory.Factory):
    license_plate = factory.Faker('license_plate')
    tariff = 'daily'

    class Meta:
        model = dict

class CarAddApi(factory.Factory):
    car = factory.Faker('license_plate')
    tariff = fuzzy.FuzzyChoice(tariffs)

    class Meta:
        model = dict

