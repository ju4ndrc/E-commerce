from fastapi import Depends, HTTPException,status

from app.auth.current_user import get_current_user
from models import RoleEnum, User


def require_role(role:RoleEnum):
    async def role_auth(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user
    return role_auth