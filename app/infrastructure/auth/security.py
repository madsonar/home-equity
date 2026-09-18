"""JWT + bcrypt + dependencies de role para FastAPI."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.infrastructure.db.models import Role, User
from app.infrastructure.db.session import get_db


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# tokenUrl relativo — o frontend faz POST em /api/v1/auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def hash_password(plain: str) -> str:
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _pwd_context.verify(plain, hashed)
    except Exception:
        return False


def create_access_token(*, user_id: int, email: str, role: Role) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role.value,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_expires_min)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Token inválido: {e}")


def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Autenticação obrigatória")
    payload = decode_token(token)
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário não encontrado")
    return user


def require_role(*allowed: Role):
    def dep(user: Annotated[User, Depends(get_current_user)]) -> User:
        # admin herda permissões de analista e cliente
        if user.role == Role.admin:
            return user
        if user.role not in allowed:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Permissão insuficiente")
        return user
    return dep


# Atalhos
def require_client(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role not in (Role.cliente, Role.admin):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Apenas clientes")
    return user


def require_analyst(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role not in (Role.analista, Role.admin):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Apenas analistas")
    return user


def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role != Role.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Apenas admin")
    return user


def current_user_from_token(token: str, db: Session) -> User:
    """Para autenticação via WebSocket (query string)."""
    payload = decode_token(token)
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário não encontrado")
    return user
