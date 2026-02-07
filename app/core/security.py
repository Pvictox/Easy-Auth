from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.schemas.token_schema import TokenAuthenticatedData
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Tuple
from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=[settings.CRYPT_CONTEXT_SCHEMES], deprecated="auto")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth_scheme)) -> TokenAuthenticatedData:
    
    #Base exception to return in case of any failure
    #TODO: Create custom exceptions
    base_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_uid: str | None = payload.get("uid")
        perfil: str | None = payload.get("perfil")
        if user_uid is None or perfil is None:
            raise base_exception
        token_data = TokenAuthenticatedData(uid=user_uid, perfil=perfil)
        return token_data
    except Exception as e:
        raise base_exception


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(user_uid: str, perfil: str) -> str:
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        #"exp": int(expire.timestamp()),
        "uid": user_uid,
        "perfil": perfil,
    }

    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token() -> Tuple[str, int]:
    new_expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    token = secrets.token_urlsafe(32)
    return token, int(new_expire.timestamp())