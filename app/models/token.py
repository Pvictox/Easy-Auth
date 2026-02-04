from typing import TYPE_CHECKING, Optional
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models import UsuarioModel


class TokenModel(SQLModel, table=True):
    __tablename__ : str = "tokens"

    id_token: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(index=True, nullable=False, unique=True)
    exp: datetime = Field(nullable=False, default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(nullable=False, default_factory=lambda: datetime.now(timezone.utc))

    is_revoked: bool = Field(default=False, nullable=False)

    usuario_id: int = Field(foreign_key="usuario.id_usuario", nullable=False)

    #Relationships

    usuario: "UsuarioModel" = Relationship(back_populates="tokens")
