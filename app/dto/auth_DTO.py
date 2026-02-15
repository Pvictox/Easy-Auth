from pydantic import BaseModel
from dataclasses import dataclass

from app.dto.usuario_DTO import UsuarioTokenDTO



class TokenAuthenticatedDataDTO(BaseModel):
    '''
     DTO for data extracted from a validated token.
    '''
    user: UsuarioTokenDTO