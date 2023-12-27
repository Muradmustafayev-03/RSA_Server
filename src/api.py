from fastapi import FastAPI, WebSocket, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.websockets import WebSocketDisconnect

from src.kdc import User

app = FastAPI()

# This is a simplistic representation. In a real-world scenario, you would use a database for user management.
users_db = {}

# OAuth2 for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# WebSocket connections storage
websocket_connections = {}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = users_db.get(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


@app.post("/register/{username}")
async def register_user(username: str, password: str):
    # Create a new user and store it in the database
    user = User(username, password)
    users_db[username] = user
    return {"message": "User registered successfully"}


@app.post("/token")
async def login_for_access_token(username: str, password: str):
    # Validate credentials and return an access token (you can use OAuth2 for this)
    user = users_db.get(username)
    if user and user.verify_password(password):
        # In a real-world scenario, you would use a more secure method to generate tokens
        token = username
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.websocket("/ws/{username}")
async def websocket_endpoint(username: str, websocket: WebSocket, current_user: User = Depends(get_current_user)):
    await websocket.accept()
    websocket_connections[username] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            # Handle data received from the websocket, e.g., establish sessions and exchange messages
            # Use the methods from your KDC module

            # Example: establish session
            if data.startswith("SESSION"):
                _, receiver_username, receiver_public_key = data.split()
                encoded_session_key = current_user.establish_session_as_sender(receiver_username, receiver_public_key)
                await websocket.send_text(f"SESSION {receiver_username} {encoded_session_key}")

            # Example: secure message exchange
            elif data.startswith("MESSAGE"):
                _, receiver_username, message = data.split()
                ciphertext = current_user.send_message(receiver_username, message)
                await websocket.send_text(f"MESSAGE {receiver_username} {ciphertext}")

    except WebSocketDisconnect:
        del websocket_connections[username]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
