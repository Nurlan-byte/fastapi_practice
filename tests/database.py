import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db, settings
from app.main import app

engine = create_engine(settings.database_url + "_test")

TestingSessionLocal = sessionmaker(engine, autoflush=False)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def overrides_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrides_get_db
    yield TestClient(app)
