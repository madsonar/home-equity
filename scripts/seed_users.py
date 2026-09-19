"""Cria usuários de demonstração. Idempotente.

As senhas vêm do ambiente (SEED_*_PASSWORD), definido no .env.prod e injetado
pelo docker-compose. Os defaults só existem para desenvolvimento local.
Com SEED_FORCE_PASSWORD=1 a senha de um usuário já existente é atualizada —
necessário para rotacionar credenciais sem recriar o banco.
"""
import os
import sys

from app.infrastructure.db.models import Role, User
from app.infrastructure.db.session import init_db, session_scope
from app.infrastructure.auth.security import hash_password


ADMIN_PWD = os.getenv("SEED_ADMIN_PASSWORD", "admin123")
ANALISTA_PWD = os.getenv("SEED_ANALISTA_PASSWORD", "analista123")
CLIENTE_PWD = os.getenv("SEED_CLIENTE_PASSWORD", "cliente123")
FORCE = os.getenv("SEED_FORCE_PASSWORD", "0") == "1"

USERS = [
    ("admin@homeequity.local", ADMIN_PWD, "Admin Principal", Role.admin),
    ("analista1@homeequity.local", ANALISTA_PWD, "Ana Analista", Role.analista),
    ("analista2@homeequity.local", ANALISTA_PWD, "Bruno Backoffice", Role.analista),
    ("cliente1@homeequity.local", CLIENTE_PWD, "Ana Ferreira", Role.cliente),
    ("cliente2@homeequity.local", CLIENTE_PWD, "Bruno Martins", Role.cliente),
    ("cliente3@homeequity.local", CLIENTE_PWD, "Carla Souza", Role.cliente),
]


def main() -> int:
    init_db()
    created, updated, existing = 0, 0, 0
    with session_scope() as db:
        for email, pwd, full, role in USERS:
            user = db.query(User).filter(User.email == email).first()
            if user:
                if FORCE:
                    user.password_hash = hash_password(pwd)
                    updated += 1
                else:
                    existing += 1
                continue
            db.add(User(
                email=email, password_hash=hash_password(pwd),
                full_name=full, role=role,
            ))
            created += 1
    print(f"Seed concluído: {created} criados, {updated} atualizados, {existing} já existiam.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
