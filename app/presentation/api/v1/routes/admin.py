from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.infrastructure.auth.security import hash_password, require_admin
from app.infrastructure.db.models import Role, User
from app.infrastructure.db.session import get_db


router = APIRouter(prefix="/admin", tags=["admin"])


class UserIn(BaseModel):
    email: str
    password: str
    full_name: str
    role: Role


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: str


@router.get("/users", response_model=list[UserOut])
def list_users(
    _: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    rows = db.query(User).order_by(desc(User.created_at)).all()
    return [UserOut(
        id=u.id, email=u.email, full_name=u.full_name,
        role=u.role.value, created_at=u.created_at.isoformat(),
    ) for u in rows]


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserIn,
    _: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")
    u = User(
        email=data.email, password_hash=hash_password(data.password),
        full_name=data.full_name, role=data.role,
    )
    db.add(u); db.commit(); db.refresh(u)
    return UserOut(
        id=u.id, email=u.email, full_name=u.full_name,
        role=u.role.value, created_at=u.created_at.isoformat(),
    )


@router.delete("/users/{uid}")
def delete_user(
    uid: int,
    me: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    if uid == me.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Não pode apagar a si mesmo")
    u = db.get(User, uid)
    if not u:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    db.delete(u); db.commit()
    return {"status": "ok"}
