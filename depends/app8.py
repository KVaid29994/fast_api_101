#Real Example: Authentication

from fastapi import FastAPI, Depends,HTTPException,Query
from typing import Optional

app = FastAPI()

def get_current_user(token : str = Query(...), user_name : str=Query(...)):
    if token != "secret" and user_name !="kash":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username":user_name}

@app.get("/profile/")

def get_profile(user = Depends(get_current_user)):
        return {"message": f"Hello {user['username']}"}



