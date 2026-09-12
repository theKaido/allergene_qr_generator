from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import CurrentUser
from app.dependencies.database import DbSession
from app.models.auth import Auth
from app.schemas.auth import Authentification, PasswordUpdate
from app.utils.security import verify_password, hash_password, create_access_token

router = APIRouter()


@router.get("/authentification")
def get_all_user(db: DbSession):
    return db.query(Auth.id, Auth.login).all()


@router.post("/authentification")
def create_new_user(db: DbSession, body: Authentification):
    user = db.query(Auth).filter(Auth.login == body.login).first()
    if user is not None:
        raise HTTPException(status_code=409, detail="Utilisateur deja présent")
    user = Auth(login=body.login, password=hash_password(body.password), email=body.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



@router.post("/login")
def login(
    db: DbSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = db.query(Auth).filter(Auth.login == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Login ou mot de passe incorrect")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Login ou mot de passe incorrect")
    token = create_access_token({"auth_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.put("/authentification/password")
def update_password(db: DbSession, body: PasswordUpdate, current_user: CurrentUser):
    if not verify_password(plain_password=body.current_password, hashed_password=current_user.password):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    current_user.password = hash_password(body.new_password)
    db.commit()
    db.refresh(current_user)
    return {"message": "Mot de passe modifié avec succées"}