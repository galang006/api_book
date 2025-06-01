import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class Book(BaseModel):
    id: str
    title: str
    sub_title: Optional[str] = None
    status: str
    thumb: str
    summary: str
    authors: list[str]
    genres: list[str]
    nsfw: bool
    type: str
    total_chapter: int
    create_at: int
    update_at: int


BOOKS_FILE = "books.json"
BOOKS = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r", encoding='utf-8') as f:
        BOOKS = json.load(f)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app!"}


@app.get("/random-book")
async def random_book():
    return random.choice(BOOKS)


@app.get("/list-books")
async def list_books():
    return {"books": BOOKS}


@app.get("/book_by_index/{index}")
async def book_by_index(index: int):
    if index < len(BOOKS):
        return BOOKS[index]
    else:
        raise HTTPException(404, f"Book index {index} out of range ({len(BOOKS)}).")


@app.post("/add-book")
async def add_book(book: Book):
    book.id = uuid4().hex 
    json_book = jsonable_encoder(book)
    BOOKS.append(json_book)

    with open(BOOKS_FILE, "w", encoding='utf-8') as f:
        json.dump(BOOKS, f)

    return {"book_id": book.id}


@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOKS:
        if book["id"] == book_id:
            return book

    raise HTTPException(404, f"Book ID {book_id} not found in database.")
