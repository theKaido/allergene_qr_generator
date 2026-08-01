from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.database import DbSession
from app.dependencies.auth import get_current_user
from app.models.restaurant import Restaurant
from app.models.auth import Auth
from app.schemas.restaurant import RestaurantCreate


router = APIRouter()

@router.get("/restaurant")
def get_restaurant(db: DbSession, current_user: Auth = Depends(get_current_user)):
    return db.query(Restaurant).filter(Restaurant.auth_id == current_user.id).all()


@router.post("/restaurant")
def restaurant_create(db: DbSession, body: RestaurantCreate, current_user: Auth = Depends(get_current_user)):
    restaurant = Restaurant(nom = body.nom, categorie = body.categorie, auth_id = current_user.id)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.get("/restaurant/{id_restaurant}")
def get_restaurant_with_id(db: DbSession, id_restaurant: int, current_user: Auth = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == id_restaurant,
        Restaurant.auth_id == current_user.id).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    return restaurant


@router.put("/restaurant/{id_restaurant}")
def update_restaurant(
        db: DbSession,
        id_restaurant: int,
        body: RestaurantCreate,
        current_user: Auth = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == id_restaurant,
        Restaurant.auth_id == current_user.id
    ).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    if body.nom:
        restaurant.nom = body.nom
    if body.categorie:
        restaurant.categorie = body.categorie
    db.commit()
    db.refresh(restaurant)
    return restaurant


@router.delete("/restaurant/{id_restaurant}")
def delete_restaurant(db: DbSession, id_restaurant: int, current_user: Auth = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == id_restaurant,
        Restaurant.auth_id == current_user.id
    ).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant non trouvé")
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant supprimé"}