
from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base


engine = create_engine("postgresql://postgres:password123@localhost:5432/fastapi_test")

TestingSessionLocal = sessionmaker(engine, autoflush=False)



# class Base(DeclarativeBase):
#     pass


# def overrides_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = overrides_get_db





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
    #run our code before we run our test
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    #run our code after our test finishes