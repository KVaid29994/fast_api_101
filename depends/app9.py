from fastapi import FastAPI, Depends, HTTPException, Query
from contextlib import asynccontextmanager
import pandas as pd
from pydantic import BaseModel

EXCEL_PATH = "id_passwords.xlsx"  # path to your file
users = {}  # global dict

@asynccontextmanager
async def lifespan(app: FastAPI):
    global users
    try:
        df = pd.read_excel(EXCEL_PATH)
        if "username" not in df.columns or "token" not in df.columns:
            raise RuntimeError("Excel file must contain 'username' and 'token' columns")
        users = dict(zip(df["username"].astype(str), df["token"].astype(str)))
    except FileNotFoundError:
        users = {}
    yield
    # cleanup if needed


app = FastAPI(lifespan=lifespan)


class AuthParams:
    def __init__(self, token: str = Query(...), username: str = Query(...)):
        self.token = token
        self.username = username

    def validate(self):
        expected = users.get(self.username)
        if expected is None or expected != self.token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"user_name": self.username}


@app.get("/profile")
def get_profile(auth: AuthParams = Depends()):
    user = auth.validate()
    return {"message": f"Hello {user['user_name']}"}

class SignupRequest(BaseModel):
    username : str
    token : str

@app.post("/signup")
def signup(req: SignupRequest):

    global users

    if req.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")

    # add to dict
    users[req.username] = req.token
    df = pd.DataFrame(list(users.items()), columns=["username", "token"])
    df.to_excel(EXCEL_PATH, index=False)
    return {"message": f"User {req.username} registered successfully"}
