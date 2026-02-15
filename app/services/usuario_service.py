from app.repositories import UsuarioRepository
from app.schemas.usuario_schema import UsuarioFormData, UsuarioBase
from app.dto.usuario_DTO import UsuarioPublicDTO, UsuarioModelDTO
from typing import List
from app.core.security import get_password_hash
from app.log_config.logging_config import get_logger

logger = get_logger(__name__)
class UsuarioService:

    def __init__(self, session ):
        self.usuario_repository = UsuarioRepository(session=session)

    
    def create_usuario(self, data:UsuarioFormData) -> UsuarioModelDTO | None:
        try: 
            usuario = self.usuario_repository.get_usuario_by_kwargs(uid=data.uid, email=data.email)
            if usuario:
                raise ValueError("UID or Email already exists") #TODO: Custom Exception
            
            password = data.password
            hashed_pass = get_password_hash(password)
            data.password = hashed_pass

            new_usuario = self.usuario_repository.create_usuario(data=data)

            return new_usuario
        except Exception as e:
            print(f"[USUARIO SERVICE - ERROR] Failed to create usuario: {e}")
            return None


    def get_all_usuarios(self) -> List[UsuarioPublicDTO]:
        try:
            usuarios = self.usuario_repository.get_all_usuarios()
            if not usuarios:
                return []
            
            usuarios_public_dto = [
                UsuarioPublicDTO(
                **usuario.model_dump(exclude={"hashed_pass", "perfil_id", "tokens", "id_usuario"})
                )
                for usuario in usuarios
            ]
            return usuarios_public_dto
        except Exception as e:
            logger.error(f"Failed to retrieve usuarios: {e}")
            return []

