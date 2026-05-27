from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from . import models
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=hzmoipas", row_factory=dict_row)
    cursor = conn.cursor()
    print("Database connection was succesfull")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error)


@app.get("/") # get это один из методов HTTP, / это путь от наччального адреса например от http://127.0.0.1:8000 и это ожно и тоже с http://127.0.0.1:8000/
async def root(): #async  опционально 
    return {"message": "Hello World"} #формат json

@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    return {'status': "success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


class Post(BaseModel):
    title: str
    content: str
    published: bool = True 



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "favorite foods", "content": "i like pizza", "id": 2}]

def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p
        
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    # cursor.execute(f" INSERT INTO posts (title, content, published) VALUES ({new_post.title, new_post.content, mew_post.published}) " Так делать не стоит. Это создает уязвимость для SQL иньекций
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
                   RETURNING *  """,
                            (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post": post}


@app.delete("/posts/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                (post.title, post.content, post.published, id))
    
    result = cursor.fetchone()
    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    conn.commit()
    return {'data': result}

