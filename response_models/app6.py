from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import json


app = FastAPI(title="practice app")

class user_input(BaseModel):
    user_name : str
    email : EmailStr
    password : str
    full_name : Optional[str] = None
    is_active : bool
    
class user_output(BaseModel):
    id : int
    user_name : str
    email : EmailStr
    is_active : bool

with open("user_list.json") as f:
    user_data = json.load(f)

@app.get("/userinfo", response_model=List[user_output])
def get_info():
    return user_data


@app.post("/newuser", response_model = user_input, status_code= status.HTTP_201_CREATED)
def create_user(user : user_input):
    new_id = max([u["id"] for u in user_data], default=0) +1
    new_user = {
        "id": new_id,
        "user_name": user.user_name,
        "email": user.email,
        "password": user.password,
        "full_name": user.full_name
    }

    user_data.append(new_user)

    with open("user_list.json", "w") as f:
        json.dump(user_data, f, indent = 4)

    return user
    

