from src.rsa import generate_keypair, encrypt, decrypt


class KeyDistributionCenter:
    def __init__(self):
        self.users = {}  # Store user information (username, public key)

    def register_user(self, username):
        # Generate and store RSA key pair for the user
        public_key, private_key = generate_keypair()
        self.users[username] = public_key, private_key

    def get_public_key(self, username):
        # Retrieve and return the public key of the specified user
        return self.users.get(username, None)

    def generate_session_key(self, sender_username, receiver_username):
        # Generate a session key for secure communication between sender and receiver
        sender_public_key, sender_private_key = self.get_public_key(sender_username)
        receiver_public_key, receiver_private_key = self.get_public_key(receiver_username)

        # Assume a simple session key, you can replace this with a more secure key exchange algorithm
        session_key = "SecretSessionKey123"

        # Encrypt the session key with the receiver's public key
        encrypted_session_key = encrypt(session_key, receiver_public_key)

        return encrypted_session_key

    def exchange_session_key(self, sender_username, receiver_username):
        # Simulate the exchange of session keys between sender and receiver
        encrypted_session_key = self.generate_session_key(sender_username, receiver_username)

        # Decrypt the session key with the receiver's private key
        receiver_public_key, receiver_private_key = self.get_public_key(receiver_username)
        decrypted_session_key = decrypt(encrypted_session_key, receiver_private_key)

        return decrypted_session_key
