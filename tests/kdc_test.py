import unittest

from src.kdc import KeyDistributionCenter


class TestKDC(unittest.TestCase):
    def setUp(self):
        self.kdc = KeyDistributionCenter()
        self.kdc.register_user("Alice")
        self.kdc.register_user("Bob")

    def test_register_user(self):
        self.kdc.register_user("Charlie")
        self.assertIn("Charlie", self.kdc.users)

    def test_get_public_key(self):
        public_key, private_key = self.kdc.get_public_key("Alice")
        self.assertIsNotNone(public_key)
        self.assertIsNone(self.kdc.get_public_key("Eve"))

    def test_generate_session_key(self):
        session_key = self.kdc.generate_session_key("Alice", "Bob")
        self.assertEqual("SecretSessionKey123", session_key)

    def test_exchange_session_key(self):
        session_key = self.kdc.exchange_session_key("Alice", "Bob")
        self.assertEqual("SecretSessionKey123", session_key)
