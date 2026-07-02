from fastapi import APIRouter, HTTPException
from app.dependencies.database import DbSession
from app.models.allergene import Allergene
from app.schemas.allergene import AllergeneCreate


router = APIRouter()


@router.get("/allergene")
def get_allergene(db: DbSession):
    return db.query(Allergene).all()


@router.post("/allergene")
def allergene_create(db: DbSession, body: AllergeneCreate):
    allergene = Allergene(nom = body.nom)
    db.add(allergene)
    db.commit()
    db.refresh(allergene)
    return allergene


@router.get("/allergene/{id_allergene}")
def get_allergene_with_id(db: DbSession, id_allergene: int):
    allergene = db.query(Allergene).filter(Allergene.id == id_allergene).first()
    if allergene is None: 
        raise HTTPException(status_code=404, detail="Allergene non trouvé")
    return allergene


@router.put("/allergene/{id_allergene}")
def update_allergene_name(db: DbSession, id_allergene, body:AllergeneCreate):
    allergene = db.query(Allergene).filter(Allergene.id == id_allergene).first()
    if allergene is None:
        raise HTTPException(status_code=404, detail="Allergene non trouvé")
    allergene.nom = body.nom
    db.commit()
    db.refresh(allergene)
    return allergene


@router.delete("/allergene/{id_allergene}")
def remove_allergene(db: DbSession, id_allergene: int):
    allergene = db.query(Allergene).filter(Allergene.id == id_allergene).first()
    if allergene is None:
        raise HTTPException(status_code=404, detail="Allergene non trouvé")
    db.delete(allergene)
    db.commit()
    return {"message": "Allergène supprimé"}