from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field
from typing import List, Optional
import os
import json


class Book(BaseModel):
    title : str = Field(..., min_length=1, max_length=200)
    author : str = Field(..., min_length=1, max_length=200)
    isbn : str = Field(...)
    pages : int = Field(..., gt=0)
    published_year : int = Field(..., gt=1900, le =2025)
    genres : List[str]
    available : bool = True
books_db = {}
BOOKS_FILE = "books.json"

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        try:
            data = json.load(f)
            books_db = {book["isbn"]: Book(**book) for book in data}
        except json.JSONDecodeError:
            books_db = {}



app = FastAPI(title="Book Management System", version= "0.1.1")
@app.get("/")
def greet():
    return {"message":"hi Kashish"}

@app.post("/books/")
def create_book(book : Book):
    if book.isbn in books_db:
        raise HTTPException(status_code=400,detail="Book already exists")
    books_db[book.isbn] = book
    with open(BOOKS_FILE, "w") as f:
        json.dump([b.model_dump() for b in books_db.values()], f, indent=4)
    
    return {"message": "Book created", "book": book}


with open("books.json") as f:
    book_data = json.load(f)

@app.get("/search/{author}")
def find_book(author:str):
    for book in book_data:
        if book["author"] == author:
            return book
    return HTTPException(status_code=404, detail="file not found")

@app.put("/books/{isbn}")
def update_availability(isbn: str, available: bool):
    if isbn not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[isbn].available = available
    return {"message": "Updated", "book": books_db[isbn]}
