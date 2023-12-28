# Cryptography project - RSA Server

### Team members: Kamal Ahmadov, Murad Mustafayev

## How to run:
1. Clone the repository
2. Create and activate virtual environment
3. Install requirements with: `pip install -r requirements.txt`
4. Run the server with: `python3 -m src.api.py`
5. Register 2 users by sending requests to the corresponding endpoint (/register)
6. Login to get access token (/token)
7. Connect to the websocket endpoint (/ws) with the access token
8. To start a session, receiver sends a message to the server with the public key of the sender.
This message starts with START_SESSION keyword.
9. When the sender receives the public key of the receiver, he sends a message to the server with the public key of the receiver.
This message starts with SESSION_KEY keyword.
10. After that, the sender, and the receiver can send encrypted messages to each other as they share the same session key.