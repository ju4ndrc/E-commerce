from fastapi import Depends,HTTPException,status
from db import SessionDep
from app.auth.authenticate import oauth2_scheme, get_user
from app.auth.validation import decode_token
from models import User


async def get_current_user(token:str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    username = payload.get('username')
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = get_user(SessionDep,username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

def check_admin(user: User = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user