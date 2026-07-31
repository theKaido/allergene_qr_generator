from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    nom: str
    categorie: str