from pydantic import BaseModel
from app.models.usuario_model import UsuarioModel
from datetime import datetime

class TokenAuth(BaseModel):
    expiration_time: datetime
    is_revoked: bool
    token: str
    usuario: UsuarioModel