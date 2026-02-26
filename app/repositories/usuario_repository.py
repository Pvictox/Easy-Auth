from app.models.usuario_model import UsuarioModel
from app.repositories import PerfilRepository
from app.dto.usuario_DTO import UsuarioModelDTO
from app.models.perfil_model import PerfilModel
from typing import List, Annotated
from app.schemas.usuario_schema import *
from unidecode import unidecode
from sqlmodel import Session, select, func
from app.log_config.logging_config import get_logger

logger = get_logger(__name__)
class UsuarioRepository:
    
    def __init__(self, session: Session):
        self.session = session
        self.perfil_repository = PerfilRepository(session=session)
    
    #TODO: Put in a generic base repository 
    def get_usuario_by_kwargs(self, **kwargs) -> UsuarioModelDTO | None:
        statement = select(UsuarioModel).filter_by(**kwargs)
        usuario = self.session.exec(statement).first()
        usuario_dto = UsuarioModelDTO.model_validate(usuario) if usuario else None
        if usuario_dto:
            return usuario_dto
        else:
            logger.warning(f"No usuario found with {kwargs}.")
            return None

    def get_count_usuarios(self, **kwargs) -> int:
        statement = select(func.count()).select_from(UsuarioModel).filter_by(**kwargs)
        count = self.session.exec(statement).one()
        return count    

    def get_all_usuarios_paginated(self, skip: int = 0, limit: int = 10) -> List[UsuarioModelDTO] | None:
        statement = select(UsuarioModel).offset(skip).limit(limit)
        usuarios = self.session.exec(statement).all()
        return [
            UsuarioModelDTO.model_validate(usuario)
            for usuario in usuarios
        ]


    def create_usuario(self, data: UsuarioFormData) -> UsuarioModelDTO | None:
        try: 
            perfil_nome = data.perfil
            #perfil = self.session.query(PerfilModel).filter(PerfilModel.valor == unidecode(perfil_nome.lower())).first()
            perfil = self.perfil_repository.get_perfil_by_kwargs(valor=unidecode(perfil_nome.lower()))
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