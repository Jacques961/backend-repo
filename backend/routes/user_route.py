from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import user_model
from backend.services import user_service, auth_service
from backend.data.database import get_db

router = APIRouter()

@router.get("/users", response_model = list[user_model.Get_User])
def get_users(db: Session = Depends(get_db)):
    users = user_service.get_users(db)

    if not users:
        raise HTTPException(status_code=404, detail="No Users Found")
    
    return users

@router.get("/users/{user_id}/", response_model = user_model.Get_User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    return user

@router.post("/users", response_model=user_model.Get_User)
def create_user(user: user_model.Create_User, db: Session = Depends(get_db)):
    return user_service.create_user(db,user)

@router.delete("/users/{user_id}/", response_model=user_model.Get_User)
def delete_user(user_id: int, db : Session = Depends(get_db),
                current_user: dict = Depends(auth_service.get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="You do not have permission to delete users.")
    user = user_service.remove_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")

    return user