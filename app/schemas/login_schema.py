from pydantic import BaseModel

class LoginRequest(BaseModel):
    '''
    Schema for login request data.
    '''
    uid: str
    password: str