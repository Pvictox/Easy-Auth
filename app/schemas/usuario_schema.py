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


class UsuarioFormData(BaseModel):
    '''
    Schema for receiving usuario data from form submissions, including password field.
    '''
    nome: str
    uid: str
    email: str
    perfil: str
    password: str
    