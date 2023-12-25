from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import uvicorn

from src.rsa import generate_keypair, encrypt, decrypt


PROTOCOL = 'http'
HOST = '127.0.0.1'
PORT = 8000

app = FastAPI()

# Simulated user database
users_db = {}

# OAuth2PasswordBearer for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserAuth(BaseModel):
    username: str
    password: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = users_db.get(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/register")
def register(user_info: UserAuth):
    username = user_info.username
    password = user_info.password

    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Generate RSA key pair for the user
    public_key, private_key = generate_keypair()

    # Store the user's public key and hashed password
    users_db[username] = {"password": password, "public_key": public_key, "private_key": private_key}

    return {"message": "User registered successfully"}


@app.post("/token")
def login(user_info: UserAuth):
    username = user_info.username
    password = user_info.password

    user = users_db.get(username)
    if user is None or user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Hash the username with the user's public key
    access_token = ''.join(encrypt(username, user["public_key"]))

    return {"access_token": access_token, "token_type": "bearer"}


def start_server():
    uvicorn.run("src.api:app", host=HOST, port=PORT)


if __name__ == "__main__":
    start_server()
