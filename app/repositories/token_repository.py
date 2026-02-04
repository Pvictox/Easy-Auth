from datetime import datetime
from app.schemas.token_schema import RefreshTokenCreate, TokenResponse
from app.models.token import TokenModel
from typing import List


class TokenRepository:
    
    def __init__(self, session):
        self.session = session


    #TODO: Put in a generic base repository 
    def get_token_by_kwargs(self, **kwargs) -> TokenModel | None:
        token = self.session.query(TokenModel).filter_by(**kwargs).first()
        if token:
            print(f"[TOKEN REPOSITORY - INFO] Retrieved token with {kwargs} from the database.")
            return token
        else:
            print(f"[TOKEN REPOSITORY - WARNING] No token found with {kwargs}.")
            return None  
        
    def get_all_tokens_by_kwargs(self, **kwargs) -> List[TokenModel] | None:
        token = self.session.query(TokenModel).filter_by(**kwargs).all()
        if token:
            print(f"[TOKEN REPOSITORY - INFO] Retrieved token with {kwargs} from the database.")
            return token
        else:
            print(f"[TOKEN REPOSITORY - WARNING] No token found with {kwargs}.")
            return None  
    
    def delete_token(self, token: TokenModel) -> None:
        try:
            self.session.delete(token)
            self.session.commit()
            print(f"[TOKEN REPOSITORY - INFO] Token deleted successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"[TOKEN REPOSITORY - ERROR] Failed to delete token: {e}")
            raise
    
    def save_refresh_token(self, refresh_token: RefreshTokenCreate) -> TokenResponse:
        # existing_tokens = self.get_all_tokens_by_kwargs(usuario_id=refresh_token.usuario_id, is_revoked=False)
        # if existing_tokens:
        #     #Revoking existing tokens before creating a new one
        #     for token in existing_tokens:
        #         token.is_revoked = True
        #         self.session.add(token)
        
        try:
            token_model = TokenModel(
                token= refresh_token.token,
                exp= datetime.fromtimestamp(refresh_token.exp),
                is_revoked= refresh_token.is_revoked,
                usuario_id= refresh_token.usuario_id
            )
            self.session.add(token_model)
            self.session.commit()
            self.session.refresh(token_model)
            return TokenResponse(
                token=refresh_token.token,
                refresh_token=refresh_token.token,
                exp=refresh_token.exp
            )
        except Exception as e:
            self.session.rollback()
            print(f"[TOKEN REPOSITORY - ERROR] Failed to create new token: {e}")
            raise 