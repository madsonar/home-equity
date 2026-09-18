from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.infrastructure.auth.security import (
    create_access_token, get_current_user, hash_password, verify_password,
)
from app.infrastructure.db.models import Role, User
from app.infrastructure.db.session import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    role: str
    full_name: str


class MeResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: Role = Role.cliente


@router.post("/login", response_model=TokenResponse)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")
    token = create_access_token(user_id=user.id, email=user.email, role=user.role)
    return TokenResponse(
        access_token=token, user_id=user.id, email=user.email,
        role=user.role.value, full_name=user.full_name,
    )


@router.get("/me", response_model=MeResponse)
def me(user: Annotated[User, Depends(get_current_user)]):
    return MeResponse(id=user.id, email=user.email, full_name=user.full_name, role=user.role.value)


@router.post("/register", response_model=MeResponse, status_code=status.HTTP_201_CREATED)
def register(
    req: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Auto-registro limitado a `cliente`. Admin/analista via seed/admin UI."""
    if req.role != Role.cliente:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Auto-registro permitido apenas para cliente")
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")
    user = User(
        email=req.email, password_hash=hash_password(req.password),
        full_name=req.full_name, role=Role.cliente,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return MeResponse(id=user.id, email=user.email, full_name=user.full_name, role=user.role.value)
