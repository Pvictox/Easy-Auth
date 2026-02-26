from app.models.perfil_model import PerfilModel
from typing import List, Annotated
from app.dto import PerfilModelDTO
from sqlmodel import Session, select
from app.log_config.logging_config import get_logger
from app.repositories.base_repository import BaseRepository

logger = get_logger(__name__)
class PerfilRepository(BaseRepository[PerfilModel, PerfilModelDTO]):
    model = PerfilModel
    dto = PerfilModelDTO

    def __init__(self, session:Session):
        super().__init__(session)
    
