from fastapi import APIRouter, HTTPException
from app.dependencies.database import DbSession
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate


router = APIRouter()


@router.get("/ingredient")
def get_ingredient(db: DbSession):
    return db.query(Ingredient).all()


@router.post("/ingredient")
def ingredient_create(db: DbSession, body: IngredientCreate):
    ingredient = Ingredient(nom = body.nom)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.get("/ingredient/{id_ingredient}")
def get_ingredient_with_id(db: DbSession, id_ingredient: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient non trouvé")
    return ingredient


@router.put("/ingredient/{id_ingredient}")
def update_ingredient_name(db: DbSession, id_ingredient: int, body: IngredientCreate):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient non trouvé")
    ingredient.nom = body.nom
    db.commit()
    db.refresh(ingredient)
    return ingredient


@router.delete("/ingredient/{id_ingredient}")
def delete_ingredient(db: DbSession, id_ingredient: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient non trouvé")
    db.delete(ingredient)
    db.commit()
    return {"message": "Ingredient supprimé"}