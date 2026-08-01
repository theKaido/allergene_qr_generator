import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    secret_key = os.getenv("JWT_SECRET_KEY")
    algo = os.getenv("JWT_ALGORITHM")
    expire_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(data["auth_id"]),
        "iat": now,
        "exp": now + timedelta(minutes=expire_minutes),
    }

    return jwt.encode(payload, secret_key, algorithm=algo)


def decode_access_token(token: str) -> dict:
    secret_key = os.getenv("JWT_SECRET_KEY")
    algo = os.getenv("JWT_ALGORITHM")

    return jwt.decode(token, secret_key, algorithms=[algo])