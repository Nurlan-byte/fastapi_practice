from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.scalars(select(models.Post)).all()
    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts



# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#             {"title": "favorite foods", "content": "i like pizza", "id": 2}]

# def find_post(id: int):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(f" INSERT INTO posts (title, content, published) VALUES ({new_post.title, new_post.content, mew_post.published}) " Так делать не стоит. Это создает уязвимость для SQL иньекций
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
    #                RETURNING *  """,
    #                         (new_post.title, new_post.content, new_post.published))
    # post = cursor.fetchone()
    # conn.commit()
        
    post = models.Post(**new_post.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[-1]
#     return {"detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    
    post = db.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.get(models.Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #             (post.title, post.content, post.published, id))
    
    # result = cursor.fetchone()
    post = db.get(models.Post, id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    allowed_fields = {"title", "content", "published"}
    
    for key, value in updated_post.model_dump().items():
        if key in allowed_fields:
            setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post
