from app.repositories import UsuarioRepository
from app.schemas.usuario_schema import UsuarioFormData, UsuarioBase
from app.dto.usuario_DTO import UsuarioPublicDTO, UsuarioModelDTO
from app.schemas.paginated_schema import PaginatedResponse
from typing import List
from app.core.security import get_password_hash
from app.log_config.logging_config import get_logger

logger = get_logger(__name__)
class UsuarioService:

    def __init__(self, session ):
        self.usuario_repository = UsuarioRepository(session=session)

    
    def create_usuario(self, data:UsuarioFormData) -> UsuarioPublicDTO | None:
        try: 
            usuario = self.usuario_repository.get_by_kwargs(uid=data.uid, email=data.email)
            if usuario:
                raise ValueError("UID or Email already exists") #TODO: Custom Exception
            
            password = data.password
            hashed_pass = get_password_hash(password)
            data.password = hashed_pass

            new_usuario = self.usuario_repository.create_usuario(data=data)

            if new_usuario:
                usuario_public_dto = UsuarioPublicDTO(
                    **new_usuario.model_dump(exclude={"hashed_pass", "perfil_id", "tokens", "id_usuario"})
                )
                return usuario_public_dto
        except Exception as e:
            print(f"[USUARIO SERVICE - ERROR] Failed to create usuario: {e}")
            return None

    def get_total_usuarios(self) -> int:
        try:
            total = self.usuario_repository.get_count()
            return total
        except Exception as e:
            logger.error(f"Failed to count usuarios: {e}")
            return 0

    def get_all_usuarios(self, skip: int=0, limit: int=10) -> PaginatedResponse[UsuarioPublicDTO]:
        empty_reponse = PaginatedResponse(
                    items=[],
                    total_items=0,
                    total_pages=0,
                    page=(skip // limit) + 1,
                    skip=skip,
                    limit=limit
        )
        try:
            total_usuarios = self.get_total_usuarios()
            if total_usuarios == 0:
                return empty_reponse
            
            usuarios = self.usuario_repository.get_all_paginated(skip=skip, limit=limit)
            if not usuarios:
                return empty_reponse
            
            usuarios_public_dto = [
                UsuarioPublicDTO(
                **usuario.model_dump(exclude={"hashed_pass", "perfil_id", "tokens", "id_usuario"})
                )
                for usuario in usuarios
            ]
            return PaginatedResponse(
                items=usuarios_public_dto,
                total_items=total_usuarios,
                total_pages=(total_usuarios + limit - 1) // limit if limit > 0 else 1,
                page=(skip // limit) + 1,
                skip=skip,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Failed to retrieve usuarios: {e}")
            return empty_reponse

