from pydantic import BaseModel


class Authentification(BaseModel):
    login: str
    password: str
    email:str

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str