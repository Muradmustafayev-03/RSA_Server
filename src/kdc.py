import bcrypt
import string
import random

from src.rsa import generate_keypair, encrypt, decrypt


class KeyDistributionCenter:
    def __init__(self):
        self.__users = {
            # username: {"public_key": public_key, "private_key": private_key, "password_hash": password_hash}
        }

    @staticmethod
    def __hash_password(password):
        # Hash the password using a secure hashing algorithm
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    @staticmethod
    def __verify_password(input_password, stored_hash):
        # Check if the input password matches the stored hash
        return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash)

    @staticmethod
    def __generate_session_key(length: int = 20):
        # Generate a random session key of the specified length
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def __get_user_keys(self, username):
        # Retrieve and return the public key of the specified user
        if username in self.__users:
            return self.__users[username]["public_key"], self.__users[username]["private_key"]
        return None, None

    def register_user(self, username, password):
        # Verify that the user does not already exist
        if username in self.__users:
            return False

        # Hash the password
        password_hash = self.__hash_password(password)

        # Generate and store RSA key pair for the user
        public_key, private_key = generate_keypair()

        # Store the user's public key, private key, and password hash
        self.__users[username] = {"public_key": public_key, "private_key": private_key, "password_hash": password_hash}

        return True

    def verify_user(self, username, password):
        # Verify that the user exists and the password is correct
        return username in self.__users and self.__verify_password(password, self.__users[username]["password_hash"])

    def generate_session_key(self, sender_username, sender_password, receiver_username):
        # Verify that the sender exists and the password is correct
        assert self.verify_user(sender_username, sender_password), "Invalid sender username or password"

        # Generate a session key for secure communication between sender and receiver
        receiver_public_key, _ = self.__get_user_keys(receiver_username)

        # Generate a random session key
        session_key = self.__generate_session_key()

        # Encrypt the session key with the receiver's public key
        encrypted_session_key = encrypt(session_key, receiver_public_key)

        return encrypted_session_key

    def exchange_session_key(self, sender_username, sender_password, receiver_username):
        # Verify that the sender exists and the password is correct
        assert self.verify_user(sender_username, sender_password), "Invalid sender username or password"

        # Simulate the exchange of session keys between sender and receiver
        encrypted_session_key = self.generate_session_key(sender_username, sender_password, receiver_username)

        # Decrypt the session key with the receiver's private key
        _, receiver_private_key = self.__get_user_keys(receiver_username)
        decrypted_session_key = decrypt(encrypted_session_key, receiver_private_key)

        return decrypted_session_key
