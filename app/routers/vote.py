from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/votes", 
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(new_vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):

    post = db.get(models.Post, new_vote.post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {new_vote.post_id} does not exist"
        )

    vote = db.scalar(select(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == new_vote.post_id))
    
    if new_vote.sign == 1:
        if vote != None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {new_vote.post_id}")
        
        add_vote = models.Vote(user_id=current_user.id, post_id=new_vote.post_id)
        db.add(add_vote)
        db.commit()
        return {"message": "succesfully added vote"}
    else:
        if vote == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")

        db.delete(vote)
        db.commit()
        return {"message": "succesfully deleted vote"}