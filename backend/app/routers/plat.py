from fastapi import APIRouter, HTTPException
from app.dependencies.database import DbSession
from app.models.plat import Plat
from app.models.restaurant import Restaurant
from app.schemas.plat import PlatCreate
from app.dependencies.auth import CurrentUser


router = APIRouter()


@router.get("/plat")
def get_plat(db: DbSession, current_user: CurrentUser):
    return db.query(Plat).join(Restaurant).filter(Restaurant.auth_id == current_user.id).all()


@router.post("/plat")
def create_plat(db: DbSession, body: PlatCreate, current_user: CurrentUser):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == body.id_restaurant,
        Restaurant.auth_id == current_user.id
    ).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Id_restaurant non trouvé")
    plat = Plat(nom = body.nom, categorie = body.categorie, id_restaurant = body.id_restaurant)
    db.add(plat)
    db.commit()
    db.refresh(plat)
    return plat


@router.get("/plat/{id_plat}")
def get_plat_with_id(db: DbSession, id_plat: int, current_user: CurrentUser):
    plat = db.query(Plat).join(Restaurant).filter(
        Plat.id == id_plat,
        Restaurant.auth_id == current_user.id
    ).first()
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat non trouvé")
    return plat


@router.put("/plat/{id_plat}")
def update_plat(db: DbSession, id_plat: int, current_user: CurrentUser, body: PlatCreate):
    plat = db.query(Plat).join(Restaurant).filter(
        Plat.id == id_plat,
        Restaurant.auth_id == current_user.id
    ).first()
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat non trouvé")
    if body.nom:
        plat.nom = body.nom
    if body.categorie:
        plat.categorie = body.categorie
    db.commit()
    db.refresh(plat)
    return plat


@router.delete('/plat/{id_plat}')
def delete_plat(db: DbSession, id_plat: int, current_user: CurrentUser):
    plat = db.query(Plat).join(Restaurant).filter(
        Plat.id == id_plat,
        Restaurant.auth_id == current_user.id
    ).first()
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat non trouvé")
    db.delete(plat)
    db.commit()
    return {"message": "Plat supprimé"}
