from app.models.usuario_model import UsuarioModel
from app.repositories import PerfilRepository
from app.dto.usuario_DTO import UsuarioModelDTO
from app.schemas.usuario_schema import *
from unidecode import unidecode
from sqlmodel import Session
from app.log_config.logging_config import get_logger
from app.repositories.base_repository import BaseRepository

logger = get_logger(__name__)
class UsuarioRepository(BaseRepository[UsuarioModel, UsuarioModelDTO]):
    model = UsuarioModel
    dto = UsuarioModelDTO
    
    def __init__(self, session: Session):
        super().__init__(session)
        self.perfil_repository = PerfilRepository(session=session)
    
    def create_usuario(self, data: UsuarioFormData) -> UsuarioModelDTO | None:
        try: 
            perfil_nome = data.perfil
            perfil = self.perfil_repository.get_by_kwargs(valor=unidecode(perfil_nome.lower()))
            if not perfil:
                logger.error(f"[USUARIO REPOSITORY - ERROR] Perfil '{perfil_nome}' not found. Cannot create usuario.")
                return None
            new_usuario = UsuarioModel(nome=data.nome, perfil_id=perfil.id_perfil, uid=data.uid, email=data.email, hashed_pass=data.password)
            self.session.add(new_usuario)
            self.session.commit()
            self.session.refresh(new_usuario)
            logger.warning(f"New usuario created with id {new_usuario.id_usuario}.")
            usuario_return = UsuarioModelDTO.model_validate(new_usuario)
            return usuario_return
        except Exception as e:
            self.session.rollback()
            logger.error(f"[USUARIO REPOSITORY - ERROR] Failed to create new usuario: {e}")
            return None