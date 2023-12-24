from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from rsa import generate_keypair, encrypt, decrypt

app = FastAPI()

# Simulated user database
users_db = {}

# OAuth2PasswordBearer for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = users_db.get(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/register/{username}")
def register_user(username: str, password: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Generate RSA key pair for the user
    public_key, private_key = generate_keypair()

    # Store the user's public key and hashed password
    users_db[username] = {"public_key": public_key, "password": password}

    return {"message": "User registered successfully"}


@app.post("/generate_session_key/{recipient}")
def generate_session_key(
        recipient: str,
        current_user: dict = Depends(get_current_user)
):
    # Ensure recipient exists
    if recipient not in users_db:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Retrieve the public key of the recipient
    recipient_public_key = users_db[recipient]["public_key"]

    # Generate a session key
    session_key = generate_session_key()

    # Encrypt the session key with the recipient's public key
    encrypted_session_key = encrypt(str(session_key), recipient_public_key)

    return {"encrypted_session_key": encrypted_session_key}


@app.post("/exchange_session_key/{recipient}")
def exchange_session_key(
        recipient: str,
        encrypted_session_key: list[int],
        current_user: dict = Depends(get_current_user)
):
    # Ensure recipient exists
    if recipient not in users_db:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Retrieve the private key of the current user
    current_user_private_key = current_user["private_key"]

    # Decrypt the received encrypted session key
    decrypted_session_key = decrypt(encrypted_session_key, current_user_private_key)

    # Store the session key for future communication
    users_db[recipient]["session_key"] = decrypted_session_key

    return {"message": "Session key exchanged successfully"}
