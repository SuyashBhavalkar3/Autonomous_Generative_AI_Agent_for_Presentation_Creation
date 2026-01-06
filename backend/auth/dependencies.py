from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .models import User
from .utils import decode_access_token
from utils.dependencies import get_db

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Dependency that returns the authenticated `User` based on a Bearer JWT.

    Expects `Authorization: Bearer <token>` header. The token is decoded using
    `auth.utils.decode_access_token` and the `sub` claim is used to look up the
    user in the database.
    """
    # Prefer Authorization: Bearer <token>
    token = credentials.credentials if credentials and credentials.scheme.lower() == 'bearer' else None

    # Fallback: allow token via query param `access_token` or header `x-access-token` for download fallback
    if not token:
        token = request.query_params.get('access_token') or request.headers.get('x-access-token')

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Missing subject in token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
