import os

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import CurrentUser
from app.dependencies.database import DbSession
from app.models.auth import Auth
from app.schemas.auth import Authentification, PasswordUpdate
from app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter()


@router.get("/authentification")
def get_all_user(db: DbSession):
    """Return the id and login of every registered user.

    Args:
        db: Database session.

    Returns:
        List of (id, login) pairs.

    """
    user_list = db.query(Auth.id, Auth.login).all()
    return [{"id": user.id, "login": user.login} for user in user_list]


@router.post("/authentification")
def create_new_user(db: DbSession, body: Authentification):
    """Register a new user account.

    Args:
        db: Database session.
        body: Login, password and email for the new account.

    Returns:
        The created user.

    Raises:
        HTTPException: If the login is already taken.

    """
    user = db.query(Auth).filter(Auth.login == body.login).first()
    if user is not None:
        raise HTTPException(status_code=409, detail="Utilisateur deja présent")
    user = Auth(
        login=body.login, password=hash_password(body.password), email=body.email
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(
    db: DbSession,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Authenticate a user and issue a JWT access token.

    Args:
        db: Database session.
        form_data: OAuth2 form data containing the login and password.
        response: Response object containing the JWT access token.

    Returns:
        A bearer access token.

    Raises:
        HTTPException: If the login or password is incorrect.

    """
    user = db.query(Auth).filter(Auth.login == form_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Login ou mot de passe incorrect")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Login ou mot de passe incorrect")
    token = create_access_token({"auth_id": user.id})
    expire_minute = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=expire_minute * 60,
    )
    return {"message": "Connexion réussie"}


@router.put("/authentification/password")
def update_password(db: DbSession, body: PasswordUpdate, current_user: CurrentUser):
    """Change the password of the authenticated user.

    Args:
        db: Database session.
        body: Current and new password.
        current_user: Authenticated user whose password is being changed.

    Returns:
        A confirmation message.

    Raises:
        HTTPException: If the current password is incorrect.

    """
    if not verify_password(
        plain_password=body.current_password, hashed_password=current_user.password
    ):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    current_user.password = hash_password(body.new_password)
    db.commit()
    db.refresh(current_user)
    return {"message": "Mot de passe modifié avec succès"}
