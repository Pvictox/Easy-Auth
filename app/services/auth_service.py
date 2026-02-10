from app.repositories import UsuarioRepository, TokenRepository
from fastapi.exceptions import HTTPException
from fastapi import Response
from app.schemas.login_schema import LoginRequest
from datetime import datetime
from typing import Optional
from app.schemas.token_schema import RefreshTokenCreate
from app.schemas.login_schema import SucessfulLoginResponse, LogoutResponse
from app.schemas.usuario_schema import UsuarioPublic
from app.core.config import settings
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)
from dotenv import load_dotenv
from app.log_config.logging_config import get_logger


load_dotenv() 

logger = get_logger(__name__)
class AuthService:

    def __init__(self, session ):
        self.usuario_repository = UsuarioRepository(session=session)
        self.token_repository = TokenRepository(session=session)
    
    def handle_login(self, data:LoginRequest, response: Response) -> SucessfulLoginResponse | None:
        try: 
            usuario = self.usuario_repository.get_usuario_by_kwargs(uid=data.uid)
            if not usuario or not verify_password(data.password, usuario.hashed_pass):
                return None
            if not usuario.is_active:
                raise ValueError("User is inactive") #TODO: Custom Exception
            
            usuario_public = UsuarioPublic(
                uid=usuario.uid,
                perfil=usuario.perfil.valor,
                email=usuario.email,
                is_active=usuario.is_active,
                nome = usuario.nome
            )

            access_token = create_access_token(usuario=usuario_public)
            refresh_token, expiration = create_refresh_token()
            

            refresh = self.token_repository.save_refresh_token(refresh_token=RefreshTokenCreate(
                token= refresh_token,
                exp= expiration,
                usuario_id= usuario.id_usuario
            ))

            is_production = settings.ENVIRONMENT == "production"

            logger.debug(f"Setting access_token cookie with value: {access_token}")
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=is_production,
                samesite="strict",
                max_age= int(settings.ACESS_TOKEN_EXPIRE_MINUTES) * 60 #type:ignore
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=is_production,
                samesite="strict",
                max_age= int(settings.REFRESH_TOKEN_EXPIRE_MINUTES) * 60 #type:ignore
            )

            return SucessfulLoginResponse(
                user=usuario_public,
            )

        except Exception as e:
            print(f"[AUTH SERVICE - ERROR] Failed to handle login: {e}")
            return None

    def refresh_acess_token(self, refresh_token: str, response: Response) -> SucessfulLoginResponse | None:
        try:
            stored_refresh_token = self.token_repository.get_token_by_kwargs(token = refresh_token)
            if not stored_refresh_token:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
            
            if stored_refresh_token.is_revoked:
                raise HTTPException(status_code=401, detail="Refresh token has been revoked")

            if stored_refresh_token.exp.timestamp() < datetime.now().timestamp():
                raise HTTPException(status_code=401, detail="Refresh token has expired")

            usuario = self.usuario_repository.get_usuario_by_kwargs(id_usuario=stored_refresh_token.usuario_id)
            if not usuario:
                raise HTTPException(status_code=404, detail="User not found")
            
            self.token_repository.delete_token(stored_refresh_token)

            
            usuario_public = UsuarioPublic(
                uid=usuario.uid,
                perfil=usuario.perfil.valor,
                email=usuario.email,
                is_active=usuario.is_active,
                nome = usuario.nome
            )
            
            access_token = create_access_token(usuario=usuario_public)
            new_refresh_token, expiration = create_refresh_token()

            refresh = self.token_repository.save_refresh_token(refresh_token=RefreshTokenCreate(
                token= new_refresh_token,
                exp= expiration,
                usuario_id= usuario.id_usuario
            ))

            is_production = settings.ENVIRONMENT == "production"
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=is_production,
                samesite="strict",
                max_age= int(settings.ACESS_TOKEN_EXPIRE_MINUTES) * 60 #type:ignore
            )

            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=is_production,
                samesite="strict",
                max_age= int(settings.REFRESH_TOKEN_EXPIRE_MINUTES) * 60 #type:ignore
            )

            return SucessfulLoginResponse(
                user=usuario_public,
            )
            
        except HTTPException as http_exc:
            raise http_exc


    def logout(self, response: Response,  refresh_token: Optional[str])-> LogoutResponse:
        try:
            logger.debug(f"Attempting to log out user with refresh token: {refresh_token}")
            if refresh_token:
                stored_refresh_token = self.token_repository.get_token_by_kwargs(token = refresh_token)
                if stored_refresh_token:
                    self.token_repository.delete_token(stored_refresh_token)
            
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return LogoutResponse(
                success=True,
                message="Logged out successfully"
            )
        except Exception as e:
            logger.error(f"[AUTH SERVICE - ERROR] Failed to handle logout: {e}")
            return LogoutResponse(
                success=False,
                message="Failed to log out"
            )