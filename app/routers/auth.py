from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import database, schemas, models, utils

router = APIRouter(tags = ["Authentication"])

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    
    user = db.scalars(select(models.User).where(models.User.email == user_credentials.email)).one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    #create a token
    #return token
    
    return {"token": "example token"}
    