from datetime import datetime
from app.dto import RefreshTokenCreate, TokenModelCreateDTO
from app.models.token_model import TokenModel
from app.schemas.token_schema import TokenResponse
from app.dto import TokenModelDTO
from app.log_config.logging_config import get_logger
from typing import List

logger = get_logger(__name__)
class TokenRepository:
    
    def __init__(self, session):
        self.session = session


    #TODO: Put in a generic base repository 
    def get_token_by_kwargs(self, **kwargs) -> TokenModelDTO | None:
        token = self.session.query(TokenModel).filter_by(**kwargs).first()
        if token:
            return TokenModelDTO(**token.model_dump())
        else:
            logger.warning(f"No token found with {kwargs}.")
            return None  
        
    def get_all_tokens_by_kwargs(self, **kwargs) -> List[TokenModelDTO] | None:
        token = self.session.query(TokenModel).filter_by(**kwargs).all()
        if token:
            return [TokenModelDTO(**t.model_dump()) for t in token]
        else:
            logger.warning(f"No token found with {kwargs}.")
            return None  
    
    def delete_token(self, token: TokenModelDTO) -> None:
        try:
            token_to_delete = TokenModel(**token.model_dump())
            db_token = self.session.get(TokenModel, token_to_delete.id_token)
            if not db_token:
                logger.warning(f"Token with id {token_to_delete.id_token} not found in database. Cannot delete.")
                return
            self.session.delete(db_token)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"[TOKEN REPOSITORY - ERROR] Failed to delete token: {e}")
            raise
    
    def save_refresh_token(self, new_refresh_token: TokenModelCreateDTO) -> TokenResponse:
        try:
            token_model = TokenModel(**new_refresh_token.model_dump())
            self.session.add(token_model)
            self.session.commit()
            self.session.refresh(token_model)
            return TokenResponse(
                token= token_model.token,
                exp= int(token_model.exp.timestamp())
            )
        except Exception as e:
            self.session.rollback()
            print(f"[TOKEN REPOSITORY - ERROR] Failed to create new token: {e}")
            raise 