from app.core.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Tuple
from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=[settings.CRYPT_CONTEXT_SCHEMES], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(user_uid: str, perfil: str) -> str:
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": int(expire.timestamp()),
        "uid": user_uid,
        "perfil": perfil,
    }

    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token() -> Tuple[str, int]:
    new_expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    token = secrets.token_urlsafe(32)
    return token, int(new_expire.timestamp())