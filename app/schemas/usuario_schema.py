from pydantic import BaseModel

class UsuarioBase(BaseModel):
    id_usuario: int
    nome: str
    is_active: bool
    uid: str
    email: str
    perfil_id: int

class UsuarioAuth(UsuarioBase):
    hashed_pass: str

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
    perfil: str
    password: str
    