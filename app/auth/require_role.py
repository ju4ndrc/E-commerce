from fastapi import Depends, HTTPException,status
from starlette.responses import RedirectResponse

from app.auth.current_user import get_current_user
from models import RoleEnum, User


def require_role(role:RoleEnum):
    async def role_auth(user: User = Depends(get_current_user)):
        if user.role != role:
            return RedirectResponse(url="/",status_code=302)
        return user
    return role_auth