from app.models.usuario_model import UsuarioModel
from app.models.perfil_model import PerfilModel
from typing import List, Annotated
from app.schemas.usuario_schema import *
from unidecode import unidecode

class UsuarioRepository:
    
    def __init__(self, session):
        self.session = session
    
    def get_all_usuarios(self) -> List[UsuarioPublic] | None:
        usuarios = self.session.query(UsuarioModel).all()
        print(f"[USUARIO REPOSITORY - INFO] Retrieved {len(usuarios)} usuarios from the database.")

        return [
            UsuarioPublic(
                nome= usuario.nome,
                is_active= usuario.is_active,
                perfil= usuario.perfil.valor,
                uid = usuario.uid,
                email= usuario.email,

            ) for usuario in usuarios
        ]

    def get_usuario_by_id(self, usuario_id: int) -> UsuarioPublic | None:
        usuario = self.session.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()
        if usuario:
            print(f"[USUARIO REPOSITORY - INFO] Retrieved usuario with id {usuario_id} from the database.")
        else:
            print(f"[USUARIO REPOSITORY - WARNING] No usuario found with id {usuario_id}.")
        return UsuarioPublic(
            nome= usuario.nome,
            is_active= usuario.is_active,
            perfil= usuario.perfil.valor,
            uid = usuario.uid,
            email= usuario.email, 
        ) if usuario else None
    
    def create_usuario(self, data: UsuarioFormData) -> UsuarioBase | None:
        try: 
            perfil_nome = data.perfil
            perfil = self.session.query(PerfilModel).filter(PerfilModel.valor == unidecode(perfil_nome.lower())).first()
            if not perfil:
                print(f"[USUARIO REPOSITORY - ERROR] Perfil '{perfil_nome}' not found. Cannot create usuario.")
                return None
            new_usuario = UsuarioModel(nome=data.nome, is_active=data.is_active, perfil_id=perfil.id_perfil, uid=data.uid, email=data.email)
            self.session.add(new_usuario)
            self.session.commit()
            self.session.refresh(new_usuario)
            print(f"[USUARIO REPOSITORY - INFO] Created new usuario with id {new_usuario.id_usuario}.")
            usuario_return = UsuarioBase(
                id_usuario=new_usuario.id_usuario ,
                nome=new_usuario.nome,
                is_active=new_usuario.is_active,
                perfil_id=new_usuario.perfil_id,
                uid = new_usuario.uid,
                email= new_usuario.email,
            )
            return usuario_return
        except Exception as e:
            self.session.rollback()
            print(f"[USUARIO REPOSITORY - ERROR] Failed to create new usuario: {e}")
            return None