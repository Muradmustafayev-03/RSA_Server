import unittest
import random

from src.rsa import encrypt
from src.kdc import Session, User
from tests.utils import generate_random_message


class TestSession(unittest.TestCase):
    def setUp(self) -> None:
        self.sender_username = 'sender'
        self.receiver_username = 'receiver'
        self.session_key = generate_random_message(32).encode()

        self.session = Session(self.sender_username, self.receiver_username, self.session_key)

    def test_is_active(self):
        self.assertTrue(self.session.is_active)

    def test_close(self):
        self.session.close()
        self.assertFalse(self.session.is_active)

    def test_encrypt_message(self):
        for _ in range(100):
            message = generate_random_message()
            ciphertext = self.session.encrypt_message(message)
            self.assertNotEqual(message, ciphertext)

    def test_decrypt_message(self):
        for _ in range(100):
            message = generate_random_message()
            ciphertext = self.session.encrypt_message(message)
            self.assertEqual(message, self.session.decrypt_message(ciphertext))


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.username = 'user'
        self.password = 'password'
        self.user = User(self.username, self.password)

    def test_verify_password(self):
        self.assertTrue(self.user.verify_password(self.password))

    def test_generate_session_key(self):
        for _ in range(10):
            salt = generate_random_message().encode()
            session_key = self.user.generate_session_key(self.username, salt)
            self.assertEqual(64, len(session_key))

    def test_establish_session(self):
        for _ in range(10):
            receiver_username = generate_random_message()
            receiver_public_key = random.randint(10, 99), random.randint(10, 99)
            encoded_session_key = self.user.establish_session_as_sender(receiver_username, receiver_public_key)
            self.assertIsNotNone(encoded_session_key)

    def test_establish_session_as_receiver(self):
        for _ in range(10):
            sender_username = generate_random_message()
            encryption_key = random.randint(10, 99), random.randint(10, 99)
            session_key = generate_random_message(64)

            encoded_session_key = encrypt(session_key, encryption_key)
            self.user.establish_session_as_receiver(sender_username, encoded_session_key)

    def test_send_and_receive_message(self):
        for _ in range(1):
            receiver_username = generate_random_message()
            receiver_public_key = random.randint(10, 99), random.randint(10, 99)
            self.user.establish_session_as_sender(receiver_username, receiver_public_key)

            message = generate_random_message()
            ciphertext = self.user.send_message(receiver_username, message)
            self.assertIsNotNone(ciphertext)
            self.assertNotEqual(message, ciphertext)

            decrypted_message = self.user.receive_message(self.username, ciphertext)
            self.assertEqual(message, decrypted_message)


if __name__ == '__main__':
    unittest.main()
