from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.dependencies.database import DbSession
from app.models.auth import Auth
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: DbSession, token: str = Depends(oauth2_scheme)) -> Auth:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    auth_id = payload.get("sub")
    if auth_id is None:
        raise credentials_exception

    user = db.query(Auth).filter(Auth.id == auth_id).first()
    if user is None:
        raise credentials_exception

    return user