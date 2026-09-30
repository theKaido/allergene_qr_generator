from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request

from app.dependencies.database import DbSession
from app.models.auth import Auth
from app.utils.security import decode_access_token


def get_current_user(db: DbSession, request: Request) -> Auth:
    """Resolve the authenticated user from a bearer JWT token.

    Args:
        db: Database session.
        request: Incoming request, used to read the access_token cookie.

    Returns:
        The authenticated user.

    Raises:
        HTTPException: If the token is missing, expired, invalid, or doesn't match
            an existing user.


    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception
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


CurrentUser = Annotated[Auth, Depends(get_current_user)]
