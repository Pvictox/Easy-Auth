from pydantic import BaseModel

class UsuarioBase(BaseModel):
    id_usuario: int
    nome: str
    is_active: bool
    uid: str
    email: str
    perfil_id: int



class UsuarioPublic(BaseModel):
    nome: str
    is_active: bool
    uid: str
    email: str
    perfil: str

class UsuarioFormData(BaseModel):
    nome: str
    uid: str
    email: str
    is_active: bool
    perfil: str
  