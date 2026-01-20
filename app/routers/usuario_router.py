from fastapi import APIRouter, Depends, status, HTTPException, Form
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario_schema import *
from app.repositories.usuario_repository import UsuarioRepository
from app.database import Database, get_session
from typing import Annotated, List
from sqlmodel import Session
router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)


SessionDependency = Annotated[ Session, Depends(get_session) ]

@router.get("/", tags=["usuarios"], status_code=status.HTTP_200_OK, response_model=List[UsuarioPublic])
async def read_usuarios(session: SessionDependency) -> List[UsuarioPublic]:
    usuario_repository = UsuarioRepository(session=session)
    usuarios = usuario_repository.get_all_usuarios()
    if not usuarios:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No usuarios found")
    return usuarios

@router.get("/{usuario_id}", tags=["usuarios"], status_code=status.HTTP_200_OK, response_model=UsuarioPublic)
async def read_usuario(usuario_id: int, session: SessionDependency) -> UsuarioPublic:
    usuario_repository = UsuarioRepository(session=session)
    usuario = usuario_repository.get_usuario_by_id(usuario_id=usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario with id {usuario_id} not found")
    return usuario

@router.post("/", tags=["usuarios"], status_code=status.HTTP_201_CREATED, response_model=UsuarioBase)
async def create_usuario(
    data: Annotated[UsuarioFormData, Form()],
    session: SessionDependency
) -> UsuarioBase | None:
    
    usuario_repository = UsuarioRepository(session=session)
    print("[USUARIO ROUTER - INFO] Creating new usuario...")
    new_usuario = usuario_repository.create_usuario(data=data)
    if not new_usuario:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create usuario")
    return new_usuario