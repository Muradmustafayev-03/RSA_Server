import string
import unittest

from src.rsa import *


def generate_random_message(length: int = 100) -> str:
    """
    Generate a random message of the specified length.

    :param length: The length of the message to generate.
    :type length: int

    :return: A random message of the specified length.
    :rtype: str
    """
    return ''.join(random.choice(string.ascii_letters + ' ') for _ in range(length))


class TestRSA(unittest.TestCase):
    def test_is_prime(self):
        for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
            self.assertTrue(is_prime(prime))

        for non_prime in [1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]:
            self.assertFalse(is_prime(non_prime))

    def test_generate_double_digit_prime(self):
        for _ in range(100):
            n_digits = random.randint(1, 10)
            n = generate_n_digit_prime(n_digits)
            self.assertTrue(is_prime(n))
            self.assertEqual(n_digits, len(str(n)))

    def test_gcd(self):
        test_cases = {
            (2, 3): 1,
            (3, 5): 1,
            (4, 6): 2,
            (6, 9): 3,
            (10, 15): 5,
            (12, 18): 6,
            (15, 21): 3,
            (21, 28): 7,
            (24, 32): 8,
            (27, 36): 9,
        }
        for (a, b), expected in test_cases.items():
            self.assertEqual(expected, gcd(a, b))

    def test_mod_inverse(self):
        test_cases = {
            (2, 3): 2,
            (3, 5): 2,
            (2, 5): 3,
            (3, 7): 5,
            (4, 7): 2,
            (5, 7): 3,
            (7, 9): 4,
            (8, 9): 8,
            (9, 11): 5,
            (10, 11): 10,
            (11, 13): 6
        }
        for (a, m), expected in test_cases.items():
            self.assertEqual(expected, mod_inverse(a, m))

    def test_encrypt_decrypt(self):
        for _ in range(10):
            # Step 1: Generate keypair
            public_key, private_key = generate_keypair()

            for _ in range(10):
                # Step 2: Encrypt message
                message = generate_random_message()
                encrypted_message = encrypt(message, public_key)

                # Step 3: Decrypt message
                decrypted_message = decrypt(encrypted_message, private_key)

                # Step 4: Check that the decrypted message is the same as the original message
                self.assertEqual(message, decrypted_message,
                                 f'Original message: {message}\n'
                                 f'Decrypted message: {decrypted_message}\n'
                                 f'Public key: {public_key}\n'
                                 f'Private key: {private_key}\n')
