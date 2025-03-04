from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from auth import hash_password

def get_user_by_username_or_email(db: Session, username_or_email: str):
    return db.query(User).filter((User.username == username_or_email) | (User.email == username_or_email)).first()

def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

