from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.get("/", response_model=list[schemas.UserOut])
def all_users(db: Session = Depends(get_db)):
    result = db.scalars(select(models.User)).all()
    return result

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'User with id: {id} does not exist')
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    user = models.User(**new_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user