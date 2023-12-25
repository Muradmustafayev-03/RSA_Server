import unittest
import requests

from src.api import *


class TestRegistration(unittest.TestCase):
    def test_registration(self):
        username = 'user1'
        password = 'password1'

        response = requests.post(f'{PROTOCOL}://{HOST}:{PORT}/register',
                                 json={'username': username, 'password': password})

        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual({'message': 'User registered successfully'}, response.json())

    def test_registration_duplicate(self):
        username = 'user2'
        password = 'password2'

        requests.post(f'{PROTOCOL}://{HOST}:{PORT}/register',
                      json={'username': username, 'password': password})

        # Try to register the same user again
        response = requests.post(f'{PROTOCOL}://{HOST}:{PORT}/register',
                                 json={'username': username, 'password': password})

        self.assertEqual(400, response.status_code, response.text)
        self.assertEqual({'detail': 'Username already registered'}, response.json())


class TestLogin(unittest.TestCase):
    def setUp(self):
        username = 'user3'
        password = 'password3'

        requests.post(f'{PROTOCOL}://{HOST}:{PORT}/register',
                      json={'username': username, 'password': password})

    def test_login(self):
        username = 'user3'
        password = 'password3'

        response = requests.post(f'{PROTOCOL}://{HOST}:{PORT}/token',
                                 json={'username': username, 'password': password})

        self.assertEqual(200, response.status_code, response.text)
        self.assertIn('access_token', response.json(), response.text)

    def test_login_bad_username(self):
        username = 'user4'
        password = 'password4'

        response = requests.post(f'{PROTOCOL}://{HOST}:{PORT}/token',
                                 json={'username': username, 'password': password})

        self.assertEqual(401, response.status_code, response.text)
        self.assertEqual({'detail': 'Invalid credentials'}, response.json())

    def test_login_bad_password(self):
        username = 'user3'
        password = 'password4'

        response = requests.post(f'{PROTOCOL}://{HOST}:{PORT}/token',
                                 json={'username': username, 'password': password})

        self.assertEqual(401, response.status_code, response.text)
        self.assertEqual({'detail': 'Invalid credentials'}, response.json())


class TestExchangeSessionKey(unittest.TestCase):
    user1 = 'user5'
    password1 = 'password5'

    user2 = 'user6'
    password2 = 'password6'

    token1: str
    token2: str

    def setUp(self):
        # Register two users
        requests.post(f'{PROTOCOL}://{HOST}:{PORT}/register', json={'username': self.user1, 'password': self.password1})
        requests.post(f'{PROTOCOL}://{HOST}:{PORT}/register', json={'username': self.user2, 'password': self.password2})

        # Login both users
        self.token1 = requests.post(f'{PROTOCOL}://{HOST}:{PORT}/token',
                                    json={'username': self.user1, 'password': self.password1}).json()['access_token']
        self.token2 = requests.post(f'{PROTOCOL}://{HOST}:{PORT}/token',
                                    json={'username': self.user2, 'password': self.password2}).json()['access_token']


if __name__ == '__main__':
    unittest.main()
