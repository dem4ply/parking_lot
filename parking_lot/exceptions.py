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


class CarIsInParkingLotError(ParkingLotError):
    message = 'The car {} is in the parking lot.'

    def __init__(self, license_plate=None):
        message = self.message.format(license_plate)
        super().__init__(message=message)


class CannotFindCarError(ParkingLotError):
    message = 'Cannot find a car in the location {}.'

    def __init__(self, location=None):
        message = self.message.format(location)
        super().__init__(message=message)


class TariffNoExistsError(ParkingLotError):
    message = 'The tariff {} cannot be processed.'

    def __init__(self, tariff=None):
        message = self.message.format(tariff)
        super().__init__(message=message)
