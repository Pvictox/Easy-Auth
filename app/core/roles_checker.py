from fastapi import Depends, HTTPException, status
from typing import List
from app.dto import TokenAuthenticatedDataDTO
from app.core.security import get_current_user


class RolesChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_token: TokenAuthenticatedDataDTO = Depends(get_current_user) ):
        if user_token.user.perfil not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role."
            )