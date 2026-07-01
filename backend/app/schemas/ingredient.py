from pydantic import BaseModel


class IngredientCreate(BaseModel):
    nom: str