from pydantic import BaseModel


class Authentification(BaseModel):
    login: str
    password: str
    email:str