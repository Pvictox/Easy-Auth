from fastapi import Depends, HTTPException, status
from typing import List
from app.schemas.token_schema import TokenAuth


class RolesChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    #TODO: Add actual dependency to extract TokenAuth
    def __call__(self, user_token: TokenAuth = Depends() ):
        if user_token.usuario.perfil.valor not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role."
            )