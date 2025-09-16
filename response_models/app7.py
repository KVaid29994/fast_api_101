from pydantic import BaseModel , Field 
from typing import Optional , List
from fastapi import FastAPI, status
import json
from datetime import datetime


class ProductCreate(BaseModel):
    name : str = Field(..., description="Name of the product", min_length=1, max_length=100)
    price : float = Field(..., gt = 0)
    description : Optional[str]  = Field(None, max_length=500)


class ProductPublic(BaseModel):
    id : int 
    name : str
    price : float

class ProductInternal(ProductCreate):
    id : int 
    created_at: datetime

with open("product_schema.json") as f:
    product_data = json.load(f)
#POST /products/ - Returns ProductPublic, status 201
app = FastAPI(title = "product catalog")

@app.post('/products', response_model=ProductPublic, status_code= status.HTTP_201_CREATED)
def create_product(product :ProductCreate):
    new_id = max([u['id'] for u in product_data] , default = 0) +1
    new_product = { "id" : new_id,
                    "name" : product.name,
                    "price":product.price,
                    "description": product.description,
                    "created_at":datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


    }
    product_data.append(new_product)
    with open("product_schema.json","w") as f:
        json.dump(product_data,f,indent=4)

    return {"id": new_id, "name": product.name, "price": product.price}


@app.get("/getproduct",response_model= List[ProductPublic])
def getproducts():
    return product_data

