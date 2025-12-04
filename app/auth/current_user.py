from fastapi import Depends,HTTPException,status,Request
from fastapi.responses import RedirectResponse

from db import SessionDep
from app.auth.authenticate import oauth2_scheme, get_user
from app.auth.validation import decode_token
from models import User, RoleEnum


async def get_current_user(request:Request,session:SessionDep) -> User:
    token = request.cookies.get("Authorization")
    if not token:
        return RedirectResponse(url="/login")
    payload = decode_token(token)
    email = payload.get('email')
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await get_user(session,email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

def check_admin(user: User = Depends(get_current_user)):
    if user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user