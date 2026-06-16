from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings

ph = PasswordHasher()


def verify_pass(plain_pass: str, hashed_pass: str) -> bool:
    try:
        return ph.verify(hashed_pass, plain_pass)
    except VerifyMismatchError:
        return False


def get_pass_hash(password: str) -> str:
    return ph.hash(password)


def _create_token(
    data: dict, expires_delta: timedelta | None, token_type: str, default_minutes: int
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=default_minutes)
    )
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    return _create_token(
        data, expires_delta, "access", settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
