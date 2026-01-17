from fastapi import APIRouter

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", tags=["usuarios"])
async def read_usuarios():
    return [{"username": "user1"}, {"username": "user2"}]