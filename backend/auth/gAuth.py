from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .models import User
from .utils import create_access_token
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
if not GOOGLE_CLIENT_ID:
    raise RuntimeError("GOOGLE_CLIENT_ID is not set in environment")

def google_login(db: Session, token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo.get("email")
        name = idinfo.get("name")

        if not email or not name:
            raise ValueError("Email or name missing in Google token")

    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token")

    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if user and user.auth_provider != "google":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered with another method")

    if not user:
        # Create new Google user
        user = User(
            name=name,
            email=email,
            auth_provider="google",
            hashed_password=None
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Issue JWT
    token = create_access_token({"sub": user.id})
    return token