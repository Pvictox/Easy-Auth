from app.repositories import UsuarioRepository, TokenRepository
from fastapi.exceptions import HTTPException
from app.schemas.login_schema import LoginRequest
from datetime import datetime
from app.schemas.token_schema import TokenResponse, RefreshTokenCreate
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

class AuthService:

    def __init__(self, session ):
        self.usuario_repository = UsuarioRepository(session=session)
        self.token_repository = TokenRepository(session=session)
    
    def handle_login(self, data:LoginRequest) -> TokenResponse | None:
        try: 
            usuario = self.usuario_repository.get_usuario_by_kwargs(uid=data.uid)
            if not usuario or not verify_password(data.password, usuario.hashed_pass):
                return None
            if not usuario.is_active:
                raise ValueError("User is inactive") #TODO: Custom Exception
            
            perfil = usuario.perfil.valor
            access_token = create_access_token(user_uid=usuario.uid, perfil=perfil)
            
            refresh_token, expiration = create_refresh_token()

            refresh = self.token_repository.save_refresh_token(refresh_token=RefreshTokenCreate(
                token= refresh_token,
                exp= expiration,
                usuario_id= usuario.id_usuario
            ))


            return TokenResponse(
                token=access_token,
                refresh_token=refresh_token,
                exp=expiration
            )

        except Exception as e:
            print(f"[AUTH SERVICE - ERROR] Failed to handle login: {e}")
            return None

    def refresh_acess_token(self, refresh_token: str) -> TokenResponse | None:
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

            
            #Generate new tokens
            perfil = usuario.perfil.valor
            access_token = create_access_token(user_uid=usuario.uid, perfil=perfil)
            new_refresh_token, expiration = create_refresh_token()
            refresh = self.token_repository.save_refresh_token(refresh_token=RefreshTokenCreate(
                token= new_refresh_token,
                exp= expiration,
                usuario_id= usuario.id_usuario
            ))
            return TokenResponse(
                token=access_token,
                refresh_token=new_refresh_token,
                exp=expiration
            )
        except HTTPException as http_exc:
            raise http_exc


        
        