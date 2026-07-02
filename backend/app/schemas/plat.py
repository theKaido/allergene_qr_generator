from pydantic import BaseModel


class PlatCreate(BaseModel):
    nom: str
    categorie: str
    id_restaurant: int
    