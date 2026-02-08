from pydantic import BaseModel

from app.schemas.usuario_schema import UsuarioPublic

class LoginRequest(BaseModel):
    '''
    Schema for login request data.
    '''
    uid: str
    password: str

class SucessfulLoginResponse(BaseModel):
    success: bool = True
    user: UsuarioPublic