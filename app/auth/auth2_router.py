from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

from app.auth.authenticate import authenticate_user
from app.auth.current_user import check_admin
from app.auth.validation import create_access_token
from db import SessionDep
from models import Token, User

router = APIRouter()

#Tutorial 🔐 Protege tu API con FastAPI: Autenticación Segura, JWT y Roles 👨‍💻🛡️ [Tutorial Completo] https://youtu.be/jOfN4jmOkcI

@router.post("/token",response_model=Token)
async def login_for_access_token(session:SessionDep,form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(session,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    access_token = create_access_token(data={"username": user.username, "role":user.role.value})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/admin/")
async def admin_route(current_user:User = Depends(check_admin)):
    return {"msg":f"{current_user.username}, Welcomer to admin panel"}