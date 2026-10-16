"""Every test runs against a throw-away SQLite file, never the PostgreSQL the app uses in Docker/Kubernetes.

DATABASE_URL has to be set before `app.config` is imported, which is why it is done at the top of this file.
"""
import os
import pathlib

TEST_DB = pathlib.Path(__file__).parent / "test.sqlite3"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    """A fresh, empty schema for each test so tests cannot depend on each other."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


def pytest_sessionfinish(session, exitstatus):
    engine.dispose()
    if TEST_DB.exists():
        TEST_DB.unlink()
