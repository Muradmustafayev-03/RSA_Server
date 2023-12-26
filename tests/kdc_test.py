import unittest

from src.kdc import KeyDistributionCenter


# class TestKDC(unittest.TestCase):
    # def setUp(self):
    #     self.kdc = KeyDistributionCenter()
    #     self.kdc.register_user("alice", "alice")
    #     self.kdc.register_user("bob", "bob")
    #
    # def test_register_user(self):
    #     self.kdc.register_user("charlie", "charlie")
    #     self.assertTrue("charlie" in self.kdc)
    #     self.assertTrue("public_key" in self.kdc._KeyDistributionCenter__users["charlie"])
    #     self.assertTrue("private_key" in self.kdc._KeyDistributionCenter__users["charlie"])
    #     self.assertTrue("password_hash" in self.kdc._KeyDistributionCenter__users["charlie"])
    #
    # def test_generate_session_key(self):
    #     encrypted_session_key = self.kdc.generate_session_key("alice", "bob")
    #     self.assertIsNotNone(encrypted_session_key)
    #
    # def test_exchange_session_key(self):
    #     encrypted_session_key = self.kdc.exchange_session_key("alice", "bob")
    #     self.assertIsNotNone(encrypted_session_key)
