## Request Handling & Data Validation
''' Pydantic Models
 Pydantic is FastAPI's data validation library. It ensures your data is correct and converts it to the right type '''

from fastapi import FastAPI
from pydantic import BaseModel,Field, EmailStr

from typing import Optional,List
from datetime import datetime
from enum import Enum

app = FastAPI()

@app.get("/")
def greet():
    return {"messgae":"Welcome"}

class CategoryEnum(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    books = "books"

class Item(BaseModel):
    name : str = Field (..., min_length=1, max_length=100, description="Item name")
    price : float = Field(..., gt=0, description="Price must be greater than 0") ## Field(..., ...) → means the field is mandatory (no default value).
    description: Optional[str] = Field(None, max_length=500)
    tax: Optional[float] = None
    tags: List[str] = []
    in_stock: bool = True
    category: CategoryEnum

 # Config with example
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "description": "High-performance laptop",
                "tax": 99.99,
                "category": "electronics",
                "tags": ["computers", "electronics"],
                "in_stock": True
            }
        }

class Review(BaseModel):
    review: str
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    reviewer_name: Optional[str] = None

@app.post("/items/") # POST is used when the client wants to send data to the server.
def create_item(item: Item): 
    total_price = item.price + (item.tax or 0)
    return {
        "message": "Item created successfully",
        "item": item,
        "total_price": total_price}
    

# PUT endpoint for updates
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "updated_item": item,
        "timestamp": datetime.now()
    }

@app.post("/items/{item_id}/reviews")
def create_review(item_id: int, review: Review):
    return {
        "item_id": item_id,
        "review": review.review,
        "rating": review.rating,
        "reviewer": review.reviewer_name or "Anonymous"
    }