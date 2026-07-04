from fastapi import APIRouter, HTTPException
from app.models.ingredient import Ingredient
from app.models.plat import Plat
from app.models.platingredient import PlatIngredient
from app.dependencies.database import DbSession


router = APIRouter()


@router.get("/restaurant/plat/{id_restaurant}")
def get_all_plat_from_restaurant(db: DbSession, id_restaurant: int):
    restaurant = db.query(Plat).filter(Plat.id_restaurant == id_restaurant).all()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant Inexistant !")
    return restaurant


@router.post("/plat/{id_plat_existant}/ingredient/{new_id_ingredient}")
def add_new_ingredient_for_plat(db: DbSession, id_plat_existant: int, new_id_ingredient: int):
    plat_ingredient_exist = db.query(PlatIngredient).filter(
        PlatIngredient.id_plat == id_plat_existant, PlatIngredient.id_ingredient == new_id_ingredient
        ).first()
    
    if plat_ingredient_exist:
        raise HTTPException(status_code=409, detail="Ingredient deja existant pour ce plat")
    
    ingredient = db.query(Ingredient).filter(Ingredient.id == new_id_ingredient).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient inexistant dans la base")
    
    plat = db.query(Plat).filter(Plat.id == id_plat_existant).first()
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat inexistant dans la base")

    new_ingredient_plat = PlatIngredient(id_ingredient = new_id_ingredient, id_plat = id_plat_existant)
    db.add(new_ingredient_plat)
    db.commit()
    db.refresh(new_ingredient_plat)
    return new_ingredient_plat

@router.delete("/plat/{id_plat}/ingredient/{id_ingredient}")
def delete_ingredient_from_plat(db: DbSession, id_plat: int, id_ingredient: int):
    ingredient_from_plat = db.query(PlatIngredient).filter(
        PlatIngredient.id_ingredient == id_ingredient,
        PlatIngredient.id_plat == id_plat
    ).first()

    if ingredient_from_plat is None:
        raise HTTPException(status_code=404, detail="L'ingredient pour ce plat n'existe pas")
    
    db.delete(ingredient_from_plat)
    db.commit()
    return {"message": "L'ingredient a bien était supprimé"}


@router.get("/plat/{id_plat}/ingredient")
def get_ingredient_for_plat(db: DbSession, id_plat: int):
    ingredient_from_plat = db.query(PlatIngredient, Ingredient).join(
        Ingredient, Ingredient.id == PlatIngredient.id_ingredient
        ).filter(
            PlatIngredient.id_plat == id_plat
            ).all()
    return [{"nom": ingredient.nom, "id_ingredient": ingredient.id} for plat_ing, ingredient in ingredient_from_plat]
