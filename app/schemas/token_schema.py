from pydantic import BaseModel
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario_schema import UsuarioPublic
from datetime import datetime

class TokenAuth(BaseModel):
    exp: int
    is_revoked: bool
    token: str
    usuario: UsuarioModel


class RefreshTokenCreate(BaseModel):
    '''
    Schema for refresh token creation.
    '''
    token: str
    exp: int
    is_revoked: bool = False
    created_at : datetime = datetime.now()
    usuario_id: int

class TokenResponse(BaseModel):
    '''
    Schema for token who will be returned to the frontend.
    '''
    token: str
    #refresh_token: str
    exp: int
    type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    '''
    Token sent by the frontend to refresh the access token.
    '''
    refresh_token: str

class TokenAuthenticatedData(BaseModel):
    '''
    Schema for data extracted from a validated token.
    '''
    user: UsuarioPublic