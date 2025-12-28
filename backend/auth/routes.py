from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.dependencies import get_db
from .schemas import UserSignup, UserLogin, TokenResponse, GoogleTokenRequest
from .service import signup_user, login_user
from .gAuth import google_login

router = APIRouter(prefix="/auth", tags=["Auth"])

# --------------------------
# Google Login
# --------------------------
@router.post("/google-login", response_model=TokenResponse)
def login_with_google(data: GoogleTokenRequest, db: Session = Depends(get_db)):
    token = google_login(db, data.google_token)
    return TokenResponse(access_token=token)


# --------------------------
# Signup
# --------------------------
@router.post("/signup", response_model=TokenResponse)
def signup(data: UserSignup, db: Session = Depends(get_db)):
    token = signup_user(db, data.name, data.email, data.password)
    return {"access_token": token}


# --------------------------
# Login
# --------------------------
@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, data.email, data.password)
    return {"access_token": token}
