from fastapi import APIRouter, Depends, status, HTTPException, Form
from app.core.roles_checker import RolesChecker
from app.dto.usuario_DTO import UsuarioPublicDTO, UsuarioModelDTO
from app.dto import TokenAuthenticatedDataDTO
from app.schemas.usuario_schema import *
from app.repositories.usuario_repository import UsuarioRepository #TODO: Remove if not used
from app.database import Database, get_session
from app.core.security import get_current_user
from typing import Annotated, List
from sqlmodel import Session
from app.services.usuario_service import UsuarioService
from app.log_config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)


_admin_required = RolesChecker(allowed_roles=["admin"])
_usuario_required = RolesChecker(allowed_roles=["usuario"])

SessionDependency = Annotated[ Session, Depends(get_session) ]

@router.get("/", tags=["usuarios"], status_code=status.HTTP_200_OK, response_model=List[UsuarioPublicDTO])
async def read_usuarios(session: SessionDependency, current_user = Depends(get_current_user)) -> List[UsuarioPublicDTO]:
    usuario_service = UsuarioService(session=session)
    usuarios = usuario_service.get_all_usuarios()
    return usuarios


@router.get("/total", tags=["usuarios"], status_code=status.HTTP_200_OK)
async def get_total_usuarios(session: SessionDependency, current_user = Annotated[TokenAuthenticatedDataDTO,Depends(get_current_user)]) -> dict:
    usuario_service = UsuarioService(session=session)
    total = usuario_service.get_total_usuarios()
    return {'success': True, 'total': total}

# @router.get("/{usuario_id}", tags=["usuarios"], status_code=status.HTTP_200_OK, response_model=UsuarioPublic)
# async def read_usuario(usuario_id: int, session: SessionDependency) -> UsuarioPublic:
#     usuario_repository = UsuarioRepository(session=session)
#     usuario = usuario_repository.get_usuario_by_kwargs(usuario_id=usuario_id)
#     if not usuario:
#         logger.warning(f"Usuario with id {usuario_id} not found in the database.")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario with id {usuario_id} not found")
#     return usuario

# @router.post("/", tags=["usuarios"], status_code=status.HTTP_201_CREATED, response_model=UsuarioBase)
# async def create_usuario(
#     data: Annotated[UsuarioFormData, Form()],
#     session: SessionDependency
# ) -> UsuarioBase | None:
    
#     usuario_service = UsuarioService(session=session)
#     print("[USUARIO ROUTER - INFO] Creating new usuario...")
#     new_usuario = usuario_service.create_usuario(data=data)
#     if not new_usuario:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create usuario")
#     return new_usuario