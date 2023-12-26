from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from src.kdc import KeyDistributionCenter

app = FastAPI()
key_distribution_center = KeyDistributionCenter()

# OAuth2PasswordBearer is used for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Pydantic models for request and response
class UserRegistration(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class SessionKeyExchange(BaseModel):
    receiver_username: str


# Dependency to get the current user based on the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # You would need to implement a function to verify the token and retrieve the user from it
    # In this example, we assume a simple token validation
    if token != "fake-access-token":
        raise credentials_exception
    return token


# User registration endpoint
@app.post("/register")
def register_user(user: UserRegistration):
    success = key_distribution_center.register_user(user.username, user.password)
    if success:
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="User already exists")


# Token-based authentication endpoint
@app.post("/token")
def login_for_access_token(user: UserRegistration):
    user_verified = key_distribution_center.verify_user(user.username, user.password)
    if not user_verified:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # In a real-world scenario, you would generate a secure access token here
    access_token = "fake-access-token"
    token_type = "bearer"
    return {"access_token": access_token, "token_type": token_type}


# Session key exchange endpoint
@app.post("/session-key-exchange")
def session_key_exchange(session_key_data: SessionKeyExchange, current_user: str = Depends(get_current_user)):
    sender_username = current_user
    sender_password = "password"  # You would need to get the password securely, maybe from a token

    encrypted_session_key = key_distribution_center.generate_session_key(
        sender_username, sender_password, session_key_data.receiver_username
    )

    return {"encrypted_session_key": encrypted_session_key}
