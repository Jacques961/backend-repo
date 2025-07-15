from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from backend.models import user_model
from backend.data.database import User_db
from sqlalchemy.orm import Session 
import random
import uuid
from backend.services.auth_service import bcrypt_context

def create_user(db: Session, user:user_model.Create_User):
    random_uuid = uuid.uuid4()
    user_id = abs(random_uuid.int) % 10000

    hashed_pass = bcrypt_context.hash(user.password)

    new_user = User_db(id=user_id, name = user.name, hashed_pass=hashed_pass, is_admin=user.is_admin)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User_db).filter(User_db.name == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_pass):
        return False
    return user

def get_user_by_id(db : Session, user_id: int):
    user = db.query(User_db).filter(User_db.id == user_id).first()

    if user is None:
        return None
    
    return user

def get_users(db: Session):
    users = db.query(User_db).all()
    
    if not users:
        return None
    
    return users
    
def remove_user(db: Session, user_id: int):
    user = db.query(User_db).filter(User_db.id == user_id).first()

    if user is None:
        return None
    
    db.delete(user)
    db.commit()

    return user
