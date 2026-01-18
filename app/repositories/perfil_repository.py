from app.models.perfil_model import PerfilModel
from typing import List, Annotated
from app.schemas.perfil_schema import PerfilBase, PerfilPublic, PerfilFormData

class PerfilRepository:
    
    def __init__(self, session):
        self.session = session
    
    def get_all_perfis(self) -> List[PerfilPublic] | None:
        perfis = self.session.query(PerfilModel).all()
        print(f"[PERFIL REPOSITORY - INFO] Retrieved {len(perfis)} perfis from the database.")
        return perfis

    def get_perfil_by_id(self, perfil_id: int) -> PerfilPublic | None:
        perfil = self.session.query(PerfilModel).filter(PerfilModel.id_perfil == perfil_id).first()
        if perfil:
            print(f"[PERFIL REPOSITORY - INFO] Retrieved perfil with id {perfil_id} from the database.")
        else:
            print(f"[PERFIL REPOSITORY - WARNING] No perfil found with id {perfil_id}.")
        return perfil
    
    def create_perfil(self, data: PerfilFormData) -> PerfilBase | None:
        try: 
            new_perfil = PerfilModel(valor=data.valor)
            self.session.add(new_perfil)
            self.session.commit()
            self.session.refresh(new_perfil)
            print(f"[PERFIL REPOSITORY - INFO] Created new perfil with id {new_perfil.id_perfil}.")

            perfil_return = PerfilBase( **new_perfil.model_dump() )
            return perfil_return
        except Exception as e:
            self.session.rollback()
            print(f"[PERFIL REPOSITORY - ERROR] Failed to create new perfil: {e}")
            return None