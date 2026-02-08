from sqlmodel import Session
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from app.database import get_session
from app.schemas.token_schema import TokenAuthenticatedData
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Tuple, Annotated
from passlib.context import CryptContext
import secrets
from app.log_config.logging_config import get_logger
from app.schemas.usuario_schema import UsuarioPublic
from app.core.cookie import CookieBearer

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=[settings.CRYPT_CONTEXT_SCHEMES], deprecated="auto")
SessionDependency = Annotated[ Session, Depends(get_session) ]
cookie_scheme = CookieBearer()

async def get_current_user(token: str = Depends(cookie_scheme)) -> TokenAuthenticatedData:
    
    #TODO: Create custom exceptions
    base_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = payload.get("user")
        if user is None:
            raise base_exception
        token_data = TokenAuthenticatedData(user=UsuarioPublic.model_validate_json(user))
        return token_data
    except JWTError as e:
        logger.error(f"JWT decoding error: {str(e)}")
        raise base_exception
    except Exception as e:
        raise base_exception


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(usuario: UsuarioPublic) -> str:
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "exp": int(expire.timestamp()),
        "user": usuario.model_dump_json()
    }

    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token() -> Tuple[str, int]:
    new_expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    token = secrets.token_urlsafe(32)
    return token, int(new_expire.timestamp())