from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.data.database import get_db
from backend.models import user_model
from backend.services import user_service, auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    
    user = user_service.authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = auth_service.create_access_token(user.name, user.id, user.is_admin, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}