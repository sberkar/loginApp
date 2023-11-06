from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    email: str
    passwd: str

class LoginUser(BaseModel):
    email: str
    passwd: str