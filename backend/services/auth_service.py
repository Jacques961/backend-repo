from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status
import secrets
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

secret_key = "dpskxq4dzGzX0nPZpz7KpOnk9oNDZJqCcEIBX88dFSP3ljtZHyTSLtpZJ0yy7JCGkItguwXxv_3JTNvDtgAlRw"
algorithm = "HS256"
access_token_expire_minutes = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(username: str, user_id:int, is_admin:bool, expires_delta:timedelta):
    encode = {'sub': username, "id": user_id, "is_admin": is_admin}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, secret_key, algorithm=algorithm)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        print("Decoded JWT payload:", payload)  
        name: str = payload.get('sub')
        user_id: int = payload.get('id')
        is_admin: bool = payload.get('is_admin')
        if name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': name, 'id': user_id, "is_admin": is_admin}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

def get_current_admin(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user