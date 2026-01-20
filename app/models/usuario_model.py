from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.perfil_model import PerfilModel

class UsuarioModel(SQLModel, table=True):
    __tablename__ : str = "usuario"

    id_usuario: int = Field(default=None, primary_key=True)
    nome: str = Field(nullable=False)
    is_active : bool = Field(default=True, nullable=False)

    #Foreign key to PerfilModel
    perfil_id: int = Field(default=None, foreign_key="perfis.id_perfil", nullable=False)

    #Relationships
    perfil: Optional["PerfilModel"] = Relationship(back_populates="usuarios")