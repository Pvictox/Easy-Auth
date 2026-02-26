from app.models.perfil_model import PerfilModel
from typing import List, Annotated
from app.dto import PerfilModelDTO
from sqlmodel import Session, select
from app.log_config.logging_config import get_logger

logger = get_logger(__name__)
class PerfilRepository:
    
    def __init__(self, session:Session):
        self.session = session
    
    def get_all_perfis(self) -> List[PerfilModelDTO] | None:
        statement = select(PerfilModel)
        perfis = self.session.exec(statement).all()
        return [
            PerfilModelDTO(**perfil.model_dump())
            for perfil in perfis
        ]

    def get_perfil_by_kwargs(self, **kwargs) -> PerfilModelDTO | None:
        statement = select(PerfilModel).filter_by(**kwargs)
        perfil = self.session.exec(statement).first()
        perfil_dto = PerfilModelDTO.model_validate(perfil) if perfil else None
        if perfil_dto:
            return perfil_dto
        else:
            logger.warning(f"No perfil found with {kwargs}.")
            return None

    # TODO: ======= REFACTOR ALL OF THESE =========

    # def get_perfil_by_id(self, perfil_id: int) -> PerfilPublic | None:
    #     perfil = self.session.query(PerfilModel).filter(PerfilModel.id_perfil == perfil_id).first()
    #     if perfil:
    #         print(f"[PERFIL REPOSITORY - INFO] Retrieved perfil with id {perfil_id} from the database.")
    #     else:
    #         print(f"[PERFIL REPOSITORY - WARNING] No perfil found with id {perfil_id}.")
    #     return perfil
    
    # def create_perfil(self, data: PerfilFormData) -> PerfilBase | None:
    #     try: 
    #         valor_normalized = unidecode(data.valor.lower())
    #         new_perfil = PerfilModel(valor=valor_normalized)
    #         self.session.add(new_perfil)
    #         self.session.commit()
    #         self.session.refresh(new_perfil)
    #         print(f"[PERFIL REPOSITORY - INFO] Created new perfil with id {new_perfil.id_perfil}.")

    #         perfil_return = PerfilBase( **new_perfil.model_dump() )
    #         return perfil_return
    #     except Exception as e:
    #         self.session.rollback()
    #         print(f"[PERFIL REPOSITORY - ERROR] Failed to create new perfil: {e}")
    #         return None