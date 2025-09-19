# This will include register → login → get token → protected route.

from datetime import datetime , timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException,status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext
'''
CryptContext` lets you:
- Define **which hashing algorithms** you want to use (e.g., `bcrypt`, `pbkdf2_sha256`)

'''
from pydantic import BaseModel


# -----------------------------
# Config
# -----------------------------

secret_key = "Kash1sh@3210"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# -----------------------------
# App & Security Setup
# -----------------------------

app = FastAPI(title="practice app")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# Fake user database
# ---------------------------

fake_user_db = {}

class User(BaseModel):
    username : str 
    disabled : Optional[bool] = False

class UserInDB(User):
    hashed_password : str


class Token(BaseModel):
    access_token : str
    token_type : str

# -----------------------------
# Utility functions
# -----------------------------

def verfiy_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username:str):
    user = fake_user_db.get(username)
    if user:
        return UserInDB(**user)
    
def authenticate_user(username:str, password:str):
    user = get_user(username)
    if not user or not verfiy_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict, expires_delta :Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.astimezone.utc() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

async def get_current_user(token : str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(tatus_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# -----------------------------
# Routes
# -----------------------------


@app.post("/register")
def register(username: str, password: str):
    if username in fake_user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(password)
    fake_user_db[username] = {"username": username, "hashed_password": hashed_password}
    return {"msg": "User registered successfully"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}
