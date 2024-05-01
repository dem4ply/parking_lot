import factory
from factory import fuzzy
from parking_lot.parking_lot import Car as Car_model


tariffs = ['hourly', 'daily']


class Car(factory.Factory):
    car = factory.Faker('license_plate')
    tariff = fuzzy.FuzzyChoice(tariffs)
    location = factory.Faker('pyint')
    hourly_fee = factory.Faker('pyint')
    daily_fee = factory.Faker('pyint')

    class Meta:
        model = Car_model


class Car_daily_fee(Car):
    tariff = 'hourly'
    start = factory.Faker(
        'date_time_between', start_date='-15d', end_date='-1d')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class Car_daily_free(Car_daily_fee):
    start = factory.Faker(
        'date_time_between', start_date='-15m', end_date='now')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class Car_hourly_fee(Car):
    tariff = 'hourly'
    start = factory.Faker(
        'date_time_between', start_date='-15h', end_date='-1h')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class Car_hourly_free(Car_hourly_fee):
    start = factory.Faker(
        'date_time_between', start_date='-15m', end_date='now')
    finish = factory.Faker(
        'date_time_between', start_date='now', end_date='now')


class Car_add(factory.Factory):
    car = factory.Faker('license_plate')
    tariff = fuzzy.FuzzyChoice(tariffs)

    class Meta:
        model = dict


class Car_add_hourly(factory.Factory):
    car = factory.Faker('license_plate')
    tariff = 'hourly'

    class Meta:
        model = dict


class Car_add_daily(factory.Factory):
    car = factory.Faker('license_plate')
    tariff = 'daily'

    class Meta:
        model = dict
