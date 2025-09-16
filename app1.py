from fastapi import FastAPI,HTTPException
import json

app = FastAPI(title= "My first app", description="Learning FASTAPi", version="1.0.0")

with open("item.json") as f:
   items_data = json.load(f)
 # Root endpoint
@app.get("/")
def read_root():
    return {"Message":"Hello user!"}

# Path parameter example
@app.get("/items/{item_id}")
def read_item(item_id: int):
    for item in items_data:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items")
def list_items():
    return items_data

# Query parameter example
@app.get("/search")
def search_items(min_price :int =0, max_price :int =9999):
    results = [item for item in items_data if min_price<= item['price']<= max_price]
    return results