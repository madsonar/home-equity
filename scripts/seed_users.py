"""Cria usuários de demonstração. Idempotente."""
import sys

from app.infrastructure.db.models import Role, User
from app.infrastructure.db.session import init_db, session_scope
from app.infrastructure.auth.security import hash_password


USERS = [
    ("admin@cashme.local", "admin123", "Admin Principal", Role.admin),
    ("analista1@cashme.local", "analista123", "Ana Analista", Role.analista),
    ("analista2@cashme.local", "analista123", "Bruno Backoffice", Role.analista),
    ("cliente1@cashme.local", "cliente123", "Ana Ferreira", Role.cliente),
    ("cliente2@cashme.local", "cliente123", "Bruno Martins", Role.cliente),
    ("cliente3@cashme.local", "cliente123", "Carla Souza", Role.cliente),
]


def main() -> int:
    init_db()
    created, existing = 0, 0
    with session_scope() as db:
        for email, pwd, full, role in USERS:
            if db.query(User).filter(User.email == email).first():
                existing += 1
                continue
            db.add(User(
                email=email, password_hash=hash_password(pwd),
                full_name=full, role=role,
            ))
            created += 1
    print(f"Seed concluído: {created} criados, {existing} já existiam.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
