from fastapi import FastAPI, Depends, HTTPException, Header, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Fake DB
posts = [
    {"id": 1, "title": "First Post"},
    {"id": 2, "title": "Second Post"},
]


# 1. Dependency: Verify API key
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != "mysecretkey":
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return x_api_key


# 2. Dependency: Pagination parameters
class PaginationParams:
    def __init__(self, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
        self.page = page
        self.size = size


# 3. Dependency: Current user (depends on verify_api_key)
def get_current_user(api_key: str = Depends(verify_api_key)):
    # Normally decode token or fetch user from DB
    if api_key == "mysecretkey":
        return {"username": "kash", "role": "admin"}
    raise HTTPException(status_code=403, detail="User not authorized")


# Request schema
class PostCreate(BaseModel):
    title: str


# 4a. GET posts with pagination + API key
@app.get("/posts", response_model=List[dict])
def list_posts(
    pagination: PaginationParams = Depends(),
    user: dict = Depends(get_current_user),
):
    start = (pagination.page - 1) * pagination.size
    end = start + pagination.size
    return posts[start:end]


# 4b. POST create new post (requires API key and user)
@app.post("/posts")
def create_post(
    post: PostCreate,
    user: dict = Depends(get_current_user),
):
    new_id = len(posts) + 1
    new_post = {"id": new_id, "title": post.title}
    posts.append(new_post)
    return {"message": "Post created", "post": new_post}
