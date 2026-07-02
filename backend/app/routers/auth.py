from fastapi import APIRouter, HTTPException
from app.dependencies.database import DbSession
from app.models.auth import Auth
from app.schemas.auth import Authentification
from app.utils.security import verify_password, hash_password

router = APIRouter()


@router.get("/authentification")
def get_all_user(db: DbSession):
    return db.query(Auth.id, Auth.login).all()


@router.post("/authentification")
def create_new_user(db: DbSession, body: Authentification):
    user = db.query(Auth).filter(Auth.login == body.login).first()
    if user is not None:
        raise HTTPException(status_code=409, detail="Utilisateur deja présent")
    user = Auth(login = body.login, password = hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(db: DbSession, body: Authentification):
    user = db.query(Auth).filter(Auth.login == body.login).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Login ou mot de passe incorrect")
    check_password = verify_password(plain_password=body.password, hash_password=user.password)
    if check_password is False:
        raise HTTPException(status_code=401, detail="Login ou mot de passe incorrect")
    return {"message": "Connexion réussie"}

@router.put("/authentification/{login}")
def update_password(db: DbSession, login: str, body: Authentification):
    user = db.query(Auth).filter(Auth.login == body.login).first()
    check_password = verify_password(plain_password=body.password, hash_password=user.password)
    if check_password is False:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    user.password = hash_password(body.password)
    db.commit()
    db.refresh(user)
    return {"message": "Mot de passe modifié avec succées"}