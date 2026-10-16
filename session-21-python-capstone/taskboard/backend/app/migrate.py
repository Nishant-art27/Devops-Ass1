"""Run Alembic migrations safely from every backend replica.

* waits for the database to accept connections (containers often start before PostgreSQL is ready)
* takes a PostgreSQL advisory lock so two replicas starting together cannot both run CREATE TABLE
"""
import sys
import time

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from app.config import settings

LOCK_ID = 8_210_921  # any constant; every replica uses the same one


def wait_for_db(engine, attempts: int = 90, delay: float = 2.0) -> None:
    for attempt in range(1, attempts + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as exc:  # noqa: BLE001
            print(f"[migrate] database not ready ({attempt}/{attempts}): {exc.__class__.__name__}", flush=True)
            time.sleep(delay)
    print("[migrate] giving up waiting for the database", flush=True)
    sys.exit(1)


def main() -> None:
    cfg = Config("alembic.ini")
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    wait_for_db(engine)
    if engine.dialect.name != "postgresql":
        command.upgrade(cfg, "head")
        return
    with engine.connect() as conn:
        conn.execute(text("SELECT pg_advisory_lock(:id)"), {"id": LOCK_ID})
        try:
            command.upgrade(cfg, "head")
        finally:
            conn.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": LOCK_ID})
    print("[migrate] schema is at head", flush=True)


if __name__ == "__main__":
    main()
