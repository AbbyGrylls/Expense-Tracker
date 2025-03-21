from fastapi import APIRouter, HTTPException
from app.database import users_collection
from app.models import User
import bcrypt, jwt, os

router = APIRouter(prefix="/users", tags=["Users"])

SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret")  # Ensure SECRET_KEY is set

@router.post("/signup")
async def signup(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    user_data = user.dict()
    user_data["password"] = hashed_password  # Store password as a string

    await users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: User):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not bcrypt.checkpw(user.password.encode(), db_user["password"].encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = jwt.encode({"userId": str(db_user["_id"])}, SECRET_KEY, algorithm="HS256")
    user_Id = str(db_user["_id"])
    return {"token": token, "userId": user_Id}
