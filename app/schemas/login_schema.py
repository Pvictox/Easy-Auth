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

class LogoutResponse(BaseModel):
    success: bool = True
    message: str = "Logout successful"