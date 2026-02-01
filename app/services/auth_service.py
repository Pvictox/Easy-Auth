from app.repositories import UsuarioRepository
from app.schemas.usuario_schema import UsuarioFormData, UsuarioPublic
from app.schemas.login_schema import LoginRequest
from app.schemas.token_schema import TokenResponse
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

class AuthService:

    def __init__(self, session ):
        self.usuario_repository = UsuarioRepository(session=session)

    
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

            #TODO: Save refresh token in DB associated with the user

            return TokenResponse(
                token=access_token,
                refresh_token=refresh_token,
                exp=expiration
            )

        except Exception as e:
            print(f"[USUARIO SERVICE - ERROR] Failed to create usuario: {e}")
            return None


        