import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL") #type: ignore
    SECRET_KEY: str = os.getenv("SECRET_KEY") #type: ignore
    ALGORITHM: str = os.getenv("ALGORITHM") #type: ignore
    CRYPT_CONTEXT_SCHEMES: str  = os.getenv("CRYPT_CONTEXT_SCHEMES") #type: ignore
    ACESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES")) #type: ignore
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))  # 7 dias #type: ignore

settings = Settings()