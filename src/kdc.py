import bcrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.rsa import generate_keypair, encrypt, decrypt


class Session:
    def __init__(self, sender_username: str, receiver_username: str, session_key: bytes):
        self.__sender_username = sender_username
        self.__receiver_username = receiver_username
        self.__session_key = session_key
        self.__is_active = True

    @property
    def sender_username(self):
        return self.__sender_username

    @property
    def receiver_username(self):
        return self.__receiver_username

    @property
    def is_active(self):
        return self.__is_active

    def close(self):
        self.__is_active = False

    def encrypt_message(self, message):
        cipher = Cipher(
            algorithms.AES(self.__session_key[:32]), modes.CFB8(self.__session_key[:16]), backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
        return ciphertext

    def decrypt_message(self, ciphertext):
        cipher = Cipher(
            algorithms.AES(self.__session_key[:32]), modes.CFB8(self.__session_key[:16]), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = self.__hash_password(password)
        self.__public_key, self.__private_key = generate_keypair(d=2)
        self.__sessions = []

    @staticmethod
    def __hash_password(password):
        # Hash the password using a secure hashing algorithm
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, password):
        # Check if the input password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def generate_session_key(self, receiver_username, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=salt,
            length=32,
            backend=default_backend()
        )
        key = kdf.derive((self.username + receiver_username).encode())
        return key.hex()

    def establish_session_as_sender(self, receiver_username, receiver_public_key):
        session_key = self.generate_session_key(receiver_username, self.password_hash)
        session = Session(self.username, receiver_username, session_key.encode())
        self.__sessions.append(session)

        encoded_session_key = encrypt(session_key, receiver_public_key)
        return encoded_session_key

    def establish_session_as_receiver(self, sender_username, encoded_session_key):
        session_key = decrypt(encoded_session_key, self.__private_key)
        session = Session(sender_username, self.username, session_key.encode())
        self.__sessions.append(session)
        return self.__public_key

    def send_message(self, receiver_username, message):
        for session in self.__sessions:
            if session.receiver_username == receiver_username:
                return session.encrypt_message(message)
        return None

    def receive_message(self, sender_username, ciphertext):
        for session in self.__sessions:
            if session.sender_username == sender_username:
                return session.decrypt_message(ciphertext)
        return None

    def update_keys(self):
        for session in self.__sessions:
            session.close()
        self.__public_key, self.__private_key = generate_keypair(d=2)

    def clear_inactive_sessions(self):
        self.__sessions = [session for session in self.__sessions if session.is_active]
