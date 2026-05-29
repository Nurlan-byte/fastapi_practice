from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import Base, engine, get_db
from .routers import post, user


Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg.connect(
        "host=localhost dbname=fastapi user=postgres password=hzmoipas",
        row_factory=dict_row
        )
    cursor = conn.cursor()
    print("Database connection was succesfull")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/") # get это один из методов HTTP, / это путь от наччального адреса например от http://127.0.0.1:8000 и это ожно и тоже с http://127.0.0.1:8000/
async def root(): #async  опционально 
    return {"message": "Hello World"} #формат json

