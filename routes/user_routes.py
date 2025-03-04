from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserLogin, UserResponse
from utils import create_user, get_user_by_username_or_email
from auth import verify_password, create_access_token, get_current_user
from datetime import timedelta


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username_or_email(db, user.username) or get_user_by_username_or_email(db, user.email):
        raise HTTPException(status_code=400, detail="Username or Email already exists")
    
    return create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username_or_email(db, user.username_or_email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(hours=5))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile")
def profile(username: str = Depends(get_current_user)): 
    return {"message": f"Profile page of {username}"}