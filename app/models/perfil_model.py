from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import UsuarioModel
    
class PerfilModel(SQLModel, table=True):
    __tablename__ : str = "perfis"
    __table_args__ = {"schema": "auth"}

    id_perfil: Optional[int] = Field(default=None, primary_key=True)
    valor: str = Field(unique=True, index=True, nullable=False)

    #Relationships
    usuarios: list["UsuarioModel"] = Relationship(back_populates="perfil")