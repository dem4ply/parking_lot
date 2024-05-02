import unittest
from parking_lot.parking_lot_api import app, parking_lot_db
from tests.factories import CarAddApi as CarAdd


class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def get(self, url, params=None):
        response = self.client.get(f"/{url}", query_string=params,)
        return response


class TestAdd(FlaskTest):
    def get(self, params=None):
        return super().get('add', params)

    def add_car(self):
        params = CarAdd.build()
        response = self.get(params)
        return response

    def test_should_work(self):
        response = self.get()
        self.assertEqual(response.status_code, 400)
        data = response.get_data()
        self.assertTrue(data)

    def test_on_empty_params_return_400_and_the_field_required(self):
        response = self.get()
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertTrue(data)
        self.assertIn('status', data)
        self.assertIn('error', data)

        self.assertEqual(data['status'], 'error')
        self.assertEqual(
            data['error'],
            'missing car data field, missing tariff data field.')

    def test_should_not_have_default_message_error(self):
        response = self.get()
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertTrue(data)
        self.assertNotIn('message', data)

    def test_add_a_car_should_return_200(self):
        params = {'car': 'X774HY98', 'tariff': 'hourly'}
        response = self.get(params)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')

        self.assertIn('car', data)
        self.assertIn('location', data)
        self.assertIn('start', data)
        self.assertIn('tariff', data)

        self.assertIsNotNone(data['car'])
        self.assertIsNotNone(data['location'])
        self.assertIsNotNone(data['start'])
        self.assertIsNotNone(data['tariff'])

    def test_when_add_car_and_is_full_should_return_error_is_full(self):
        parking_lot_db.amount_lot = 3
        for v in list(parking_lot_db.lot.values()):
            parking_lot_db.remove(v.location)
        response = self.add_car()
        self.assertEqual(response.status_code, 200)
        response = self.add_car()
        self.assertEqual(response.status_code, 200)
        response = self.add_car()
        self.assertEqual(response.status_code, 200)
        response = self.add_car()
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('error', data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['error'], 'No free space.')

    def test_enter_the_same_car_twice_should_no_be_posible(self):
        params = {'car': 'X774HY98', 'tariff': 'hourly'}
        parking_lot_db.clear()
        response = self.get(params)
        self.assertEqual(response.status_code, 200)

        response = self.get(params)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('error', data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(
            data['error'], 'The car X774HY98 is in the parking lot.')

    def test_car_param_empty_should_return_error(self):
        params = {'car': '', 'tariff': 'hourly'}
        parking_lot_db.clear()
        response = self.get(params)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('error', data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(
            data['error'], 'field car cannot be blank.')


class TestRemove(FlaskTest):
    def get(self, location=None):
        if location is not None:
            return super().get('remove', {'location': location})
        return super().get('remove',)


class TestRemoveErrors(TestRemove):

    def test_should_work(self):
        response = self.get()
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertTrue(data)

    def test_when_dont_send_location_should_return_that_is_required(self):
        response = self.get()
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('error', data)

        self.assertEqual(data['status'], 'error')
        self.assertEqual(
            data['error'],
            'missing location data field.')


class TestRemoveNoEmpty(TestRemove):
    def get_any_car(self):
        if parking_lot_db.is_empty:
            car = parking_lot_db.add(**CarAdd.build())
        else:
            car = next(iter(parking_lot_db.lot.values()))
        return car

    def test_remove_car_should_return_the_data_of_car(self):
        car = self.get_any_car()
        response = self.get(car.location)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('car', data)
        self.assertIn('location', data)
        self.assertIn('start', data)
        self.assertIn('tariff', data)
        self.assertIn('finish', data)
        self.assertIn('fee', data)

        self.assertIsNotNone(data['car'])
        self.assertIsNotNone(data['location'])
        self.assertIsNotNone(data['start'])
        self.assertIsNotNone(data['tariff'])
        self.assertIsNotNone(data['finish'])
        self.assertIsNotNone(data['fee'])

    def test_remove_car_on_empty_spot_should_return_a_message(self):
        car = self.get_any_car()
        response = self.get(car.location)
        self.assertEqual(response.status_code, 200)
        response = self.get(car.location)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()

        self.assertTrue(data)
        self.assertIn('status', data)
        self.assertIn('error', data)

        self.assertEqual(data['status'], 'error')
        self.assertEqual(
            data['error'],
            f'Cannot find a car in the location {car.location}.')


class TestList(FlaskTest):
    def get(self):
        return super().get('list',)

    def test_should_work(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('cars', data)
        self.assertIsInstance(data['cars'], list)

        for car in data['cars']:
            self.assertTrue(data)
            self.assertIn
