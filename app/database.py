from dotenv import load_dotenv
import os

from sqlmodel import create_engine, SQLModel, text, Session

load_dotenv()  # Load environment variables from .env file

class Database():
    '''
        Database connection and setup class.
    '''
    def __init__(self):
        self.engine = None
        self.create_engine()
        pass

    def create_engine(self) -> None:
        DATABASE_URL  = os.getenv("DATABASE_URL") 

        if DATABASE_URL is None:
            raise ValueError("DATABASE_URL is not set in the environment variables.")

        self.engine = create_engine(DATABASE_URL, echo=True) if DATABASE_URL else None

    def get_engine(self) -> object:
        return self.engine

    def create_db_and_tables(self) -> None:
        if self.engine:
            SQLModel.metadata.create_all(self.engine) 
        else:
            raise ValueError("Engine is not initialized.") #TODO: Custom error handling
    
    def check_connection(self) -> bool:
        try:
            if self.engine:
                with self.engine.connect() as connection:
                    # data = connection.execute(text("SELECT * from auth.perfis")) # Simple query to test connection 
                    # for row in data:
                    #     print(row)
                    print("[DATABASE - INFO] Database connection successful.")
                return True
            else:
                print("[DATABASE - ERROR] Engine is not initialized.")
                return False
        except Exception as e:
            print(f"[DATABASE - ERROR] Database connection failed: {e}")
            return False 


db = Database()

def get_session():
        if not db.engine:
            raise ValueError("Engine is not initialized.")
        with Session(db.engine) as session:
            yield session
    