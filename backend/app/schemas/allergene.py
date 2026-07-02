from pydantic import BaseModel

class AllergeneCreate(BaseModel):
    nom: str