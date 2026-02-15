from sqlmodel import SQLModel
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class PerfilModelDTO(SQLModel):
    id_perfil: int
    valor: str

    class Config:
        from_attributes = True