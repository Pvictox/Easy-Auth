from sqlmodel import SQLModel, Field
from typing import Optional

class PerfilModel(SQLModel, table=True):
    __tablename__ : str = "perfis"

    id_perfil: Optional[int] = Field(default=None, primary_key=True)
    valor: str = Field(unique=True, index=True, nullable=False)
