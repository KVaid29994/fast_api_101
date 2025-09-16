#When you read “Response Models” in FastAPI docs or a book, it refers to Pydantic models used to shape (filter/validate) the data returned to the client.

#By default, FastAPI just returns whatever your function returns (a dict, list, etc.). But often:
#You don’t want to expose all fields of your database/model.
#You want consistent schemas for responses.
#You want FastAPI to validate & document responses in the OpenAPI docs.

'''
from pydantic import BaseModel

class UserResponse(BaseModel):
    username: str   # ✅ only expose username

@app.get("/user", response_model=UserResponse)
def get_user():
    return {"username": "kashish", "password": "secret123"}

'''

'''

And status codes just tell the client what happened:

200 OK → success

201 Created → resource created (used in POST)

404 Not Found → item missing

400 Bad Request → invalid input

500 Internal Server Error → server bug
'''

from fastapi import FastAPI, HTTPException , status
from pydantic import BaseModel, Field
from typing import List, Dict
import uuid
import json
import os


BOOKS_FILE = "books_list.json"

# with open("books_list.json") as f:
#     book_data = json.load(f)

app = FastAPI(title="Book Management System", version="1.0.1")
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=200)
    pages: int = Field(..., gt=0)
    published_year: int = Field(..., gt=1900, le=2025)

class BookCreate(BookBase):
    genres: List[str]
    available: bool = True

class BookResponse(BookBase):
    id: str
    genres: List[str]
    available: bool

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        try:
            book_data = json.load(f)
        except json.JSONDecodeError:
            book_data = []
else:
    book_data = []

books_db: Dict[str, BookResponse] = {b["id"]: BookResponse(**b) for b in book_data}

@app.get("/", status_code= status.HTTP_200_OK)
def greet():
    return {"message": "📚 Welcome to the Book Management API!"}

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book:BookCreate):
    book_id = str(uuid.uuid4())
    new_book = BookResponse(id=book_id, **book.model_dump())
    books_db[book_id] = new_book
    with open(BOOKS_FILE, "w") as f:
        json.dump([b.model_dump() for b in books_db.values()], f, indent=4)

    return new_book

@app.get("getbooks/", response_model = List[BookResponse],status_code=status.HTTP_200_OK)
def list_books():
    for books in book_data:
        return books
    
@app.get("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(book_id: str):
    for book in book_data:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")



