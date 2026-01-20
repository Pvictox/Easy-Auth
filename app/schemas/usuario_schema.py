from pydantic import BaseModel

class UsuarioBase(BaseModel):
    id_usuario: int
    nome: str
    is_active: bool
    perfil_id: int



class UsuarioPublic(BaseModel):
    nome: str
    is_active: bool
    perfil: str

class UsuarioFormData(BaseModel):
    nome: str
    is_active: bool
    perfil: str
  