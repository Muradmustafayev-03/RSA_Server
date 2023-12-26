import unittest

from src.kdc import KeyDistributionCenter


class TestKDC(unittest.TestCase):
    user1 = 'Alice', '123456'
    user2 = 'Bob', 'password'

    def setUp(self):
        self.kdc = KeyDistributionCenter()
        self.kdc.register_user(*self.user1)
        self.kdc.register_user(*self.user2)

    def test_register_user(self):
        self.assertTrue(self.kdc.verify_user(*self.user1))
        self.assertTrue(self.kdc.verify_user(*self.user2))

    def test_generate_session_key(self):
        session_key = self.kdc.generate_session_key(*self.user1, self.user2[0])
        self.assertEqual(len(session_key.split(',')), 20)

    def test_exchange_session_key(self):
        session_key = self.kdc.exchange_session_key(*self.user1, self.user2[0])
        self.assertEqual(len(session_key), 20)

        session_key = self.kdc.exchange_session_key(*self.user2, self.user1[0])
        self.assertEqual(len(session_key), 20)


if __name__ == '__main__':
    unittest.main()
