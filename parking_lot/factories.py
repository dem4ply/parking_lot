import factory
from factory import fuzzy


tariffs = [ 'hourly', 'daily' ]


class car_add( factory.Factory ):
    car = factory.Faker( 'license_plate' )
    tariff = fuzzy.FuzzyChoice( tariffs )

    class Meta:
        model = dict
