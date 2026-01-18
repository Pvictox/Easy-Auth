from fastapi import APIRouter, Depends, status, HTTPException, Form
from app.models.perfil_model import PerfilModel
from app.schemas.perfil_schema import PerfilPublic, PerfilBase, PerfilFormData
from app.repositories.perfil_repository import PerfilRepository
from app.database import Database, get_session
from typing import Annotated, List
from sqlmodel import Session


router = APIRouter(
    prefix="/perfis",
    tags=["perfis"],
    responses={404: {"description": "Not found"}},)

SessionDependency = Annotated[ Session, Depends(get_session) ]

@router.get("/", tags=["perfis"], status_code=status.HTTP_200_OK, response_model=List[PerfilPublic])
async def read_perfis(session: SessionDependency) -> List[PerfilPublic]:
    perfil_repository = PerfilRepository(session=session)
    perfis = perfil_repository.get_all_perfis()
    if not perfis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No perfis found")
    return perfis

@router.get("/{perfil_id}", tags=["perfis"], status_code=status.HTTP_200_OK, response_model=PerfilPublic)
async def get_perfil_by_id(perfil_id: int, session: SessionDependency) -> PerfilPublic:
    perfil_repository = PerfilRepository(session=session)
    perfil = perfil_repository.get_perfil_by_id(perfil_id=perfil_id)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Perfil with id {perfil_id} not found")
    return perfil

@router.post("/", tags=["perfis"], status_code=status.HTTP_201_CREATED, response_model=PerfilBase)
async def create_perfil(
    data: Annotated[PerfilFormData, Form()],
    session: SessionDependency
) -> PerfilBase | None:
    
    perfil_repository = PerfilRepository(session=session)
    print("[PERFIL ROUTER - INFO] Creating new perfil...")
    new_perfil = perfil_repository.create_perfil(data=data)
    if not new_perfil:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create perfil")
    return new_perfil