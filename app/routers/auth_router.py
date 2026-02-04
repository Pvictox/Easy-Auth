import json
from fastapi import APIRouter, Depends, status, HTTPException, Form
from app.database import Database, get_session
from app.schemas.token_schema import TokenResponse, TokenRefreshRequest
from app.schemas.login_schema import LoginRequest
from app.repositories.usuario_repository import UsuarioRepository
from typing import Annotated, List
from app.services.auth_service import AuthService
from sqlmodel import Session
from app.schemas.usuario_schema import UsuarioPublic

from app.core.security import (
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


SessionDependency = Annotated[ Session, Depends(get_session) ]


@router.post("/login",tags=["authentication"], status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(login_data: Annotated[LoginRequest, Form()], session: SessionDependency) -> TokenResponse | None:
    try:
        print("[AUTH ROUTER - INFO] Handling login request...")
        auth_service = AuthService(session=session)
        token_response = auth_service.handle_login(data=login_data)
        
        if not token_response:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid UID or password")
        
        return token_response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed.")
    
    
@router.post("/refresh", tags=["authentication"], status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def refresh_token(data: Annotated[TokenRefreshRequest, Form()], session: SessionDependency) -> TokenResponse | None:
    try:
        print("[AUTH ROUTER - INFO] Handling token refresh request...")
        auth_service = AuthService(session=session)
        token_response = auth_service.refresh_acess_token(refresh_token=data.refresh_token)
        
        if not token_response:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        return token_response
    except HTTPException as http_exc:
        raise http_exc