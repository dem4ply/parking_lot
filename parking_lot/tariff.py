from .exceptions import TariffNoExistsError


class MetaTariff(type):
    def __str__(self):
        return self.__name__.lower()


class Tariff(metaclass=MetaTariff):
    fee_cost = 0
    seconds_to_charge = 0

    @classmethod
    def resolve(cls, name):
        for tariff in all_tariff:
            if str(tariff) == name:
                return tariff
        raise TariffNoExistsError

    @classmethod
    def fee(cls, diff_time):
        # less of 15 min is free of charge
        if diff_time.total_seconds() // (60 * 15) < 1:
            return 0

        return cls.proportional_diff_time(diff_time) * cls.fee_cost

    @classmethod
    def proportional_diff_time(cls, diff_time):
        return (diff_time.total_seconds() // cls.seconds_to_charge) + 1


class Daily(Tariff):
    fee_cost = 20
    seconds_to_charge = 86400


class Hourly(Tariff):
    fee_cost = 1
    seconds_to_charge = 3600


all_tariff = [Daily, Hourly]
