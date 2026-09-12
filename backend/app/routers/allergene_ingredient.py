from fastapi import APIRouter, HTTPException
from app.models.allergeneingredient import AllergeneIngredient
from app.models.allergene import Allergene
from app.models.ingredient import Ingredient
from app.models.plat import Plat
from app.models.restaurant import Restaurant
from app.schemas.allergene_ingredient import AllergeneIngredientClass
from app.dependencies.database import DbSession
from app.dependencies.auth import CurrentUser

router = APIRouter()


@router.get("/plat/{id_plat}/ingredient/{id_ingredient}/allergene")
def get_allergene_for_ingredient(db: DbSession, id_plat: int, id_ingredient: int, current_user: CurrentUser):
    ingr_allergene = db.query(AllergeneIngredient, Allergene).join(
        Allergene, Allergene.id == AllergeneIngredient.id_allergene
    ).join(Plat).join(Restaurant).filter(
    AllergeneIngredient.id_ingredient == id_ingredient,
        AllergeneIngredient.id_plat == id_plat,
        Restaurant.auth_id == current_user.id
    ).all()

    return [
        {"nom_allergene": allergene.nom, "status": all_ing.status}
        for all_ing, allergene in ingr_allergene
    ]


@router.post("/plat/{new_id_plat}/ingredient/{new_id_ingredient}/allergenes/{new_id_allergene}")
def add_new_allergene_for_ingredient(
        db: DbSession,
        new_id_plat: int,
        new_id_ingredient: int,
        new_id_allergene:int,
        current_user: CurrentUser,
        body: AllergeneIngredientClass
):
    check_plat = db.query(Plat).join(Restaurant).filter(
        Plat.id == new_id_plat,
        Restaurant.auth_id == current_user.id
    ).first()

    if check_plat is None:
        raise HTTPException(status_code=404, detail="Plat inexistant")

    all_ingr = db.query(AllergeneIngredient).filter(
        AllergeneIngredient.id_allergene == new_id_allergene,
        AllergeneIngredient.id_ingredient == new_id_ingredient,  # ← n'oublie pas celui-là
        AllergeneIngredient.id_plat == new_id_plat 
    ).first()

    if all_ingr:
        raise HTTPException(status_code=409, detail="L'allergene pour cette ingredient est deja présent")
    
    new_all_ingr = AllergeneIngredient(
        id_plat = new_id_plat,
        id_ingredient = new_id_ingredient,
        id_allergene = new_id_allergene,
        status = body.status
    )

    db.add(new_all_ingr)
    db.commit()
    db.refresh(new_all_ingr)

    return new_all_ingr


@router.put("/plat/{id_plat}/ingredient/{id_ingredient}/allergene/{id_allergene}")
def update_status_ingredient_allergene(
        db: DbSession,
        id_plat: int,
        id_ingredient: int,
        id_allergene: int,
        current_user: CurrentUser,
        body: AllergeneIngredientClass
):

    all_ingr = db.query(AllergeneIngredient).join(Plat).join(Restaurant).filter(
        AllergeneIngredient.id_allergene == id_allergene,
        AllergeneIngredient.id_ingredient == id_ingredient,
        AllergeneIngredient.id_plat == id_plat,
        Restaurant.auth_id == current_user.id
    ).first()    

    if all_ingr is None:
        raise HTTPException(status_code=404, detail="L'allergene pour cette ingredient n'existe pas")
    
    all_ingr.status = body.status

    db.commit()
    db.refresh(all_ingr)
    
    return all_ingr


@router.delete("/plat/{id_plat}/ingredient/{id_ingredient}/allergene/{id_allergene}")
def delete_ingredient_allergene(db: DbSession, id_plat: int, id_ingredient: int, id_allergene: int, current_user: CurrentUser):
    all_ing = db.query(AllergeneIngredient).join(Plat).join(Restaurant).filter(
        AllergeneIngredient.id_allergene == id_allergene,
        AllergeneIngredient.id_ingredient == id_ingredient,
        AllergeneIngredient.id_plat == id_plat,
        Restaurant.auth_id == current_user.id
    ).first()

    if all_ing is None:
        raise HTTPException(status_code=404, detail="L'allergène pour cet ingrédient n'existe pas")

    db.delete(all_ing)
    db.commit()

    return {"message": "L'allergene lié a cette ingredient a bien été supprimé"}
