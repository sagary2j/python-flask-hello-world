import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    def test_save_user_data_success(self):
        tester = app.test_client(self)
        response = tester.put('/hello/testuser', json={'dateOfBirth': '2000-01-01'})
        self.assertEqual(response.status_code, 204)

    def test_save_user_data_invalid_username(self):
        tester = app.test_client(self)
        response = tester.put('/hello/testuser1!', json={'dateOfBirth': '2000-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username must contain only letters', response.data.decode('utf-8'))

    def test_save_user_data_invalid_date_format(self):
        tester = app.test_client(self)
        response = tester.put('/hello/testuser', json={'dateOfBirth': 'invalid'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid date format', response.data.decode('utf-8'))
    
    def test_save_user_data_future_date(self):
            with app.test_client() as client:
                response = client.put('/hello/john', json={'dateOfBirth': '2030-01-01'})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json, {'error': 'Date of birth must be in the past.'})

    def test_save_user_data_database_error(self):
        tester = app.test_client(self)
        response = tester.put('/hello/testuser', json={'dateOfBirth': '2000-01-01'})
        self.assertEqual(response.status_code, 500)
        self.assertIn('Internal server error', response.data.decode('utf-8'))

    def test_get_hello_message_user_found(self):
        tester = app.test_client(self)
        tester.put('/hello/testuser', json={'dateOfBirth': '2000-01-01'})
        response = tester.get('/hello/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, testuser!', response.data.decode('utf-8'))

    def test_get_hello_message_user_not_found(self):
        tester = app.test_client(self)
        response = tester.get('/hello/unknownuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User unknownuser not found', response.data.decode('utf-8'))

    def test_get_hello_message_birthday_today(self):
        tester = app.test_client(self)
        tester.put('/hello/testuser', json={'dateOfBirth': '2000-06-30'})
        response = tester.get('/hello/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, testuser! Happy birthday!', response.data.decode('utf-8'))

    def test_get_hello_message_birthday_in_future(self):
        tester = app.test_client(self)
        tester.put('/hello/testuser', json={'dateOfBirth': '2000-07-01'})
        response = tester.get('/hello/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, testuser! Your birthday is in 1 day(s)', response.data.decode('utf-8'))

    def test_get_hello_message_birthday_in_past(self):
        tester = app.test_client(self)
        tester.put('/hello/testuser', json={'dateOfBirth': '2000-06-29'})
        response = tester.get('/hello/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, testuser! Your birthday is in 365 day(s)', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()