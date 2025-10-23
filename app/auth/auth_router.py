from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import select
from db import SessionDep  # Tu dependencia síncrona
from models import User
from app.auth.hash import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBasic()

# Sesiones simples en memoria (solo para demostración)
current_sessions = {}

# ---- LOGIN ----
@router.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), session: SessionDep = None):
    statement = select(User).where(User.email == credentials.username)
    user = session.exec(statement).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    current_sessions[user.email] = user.role
    return {"message": f"Welcome {user.username}", "role": user.role}


# ---- LOGOUT ----
@router.post("/logout")
def logout(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username in current_sessions:
        del current_sessions[credentials.username]
        return {"message": "Logged out successfully"}
    raise HTTPException(status_code=401, detail="User not logged in")


# ---- VALIDAR USUARIO ----
def get_current_user(credentials: HTTPBasicCredentials = Depends(security), session: SessionDep = None):
    statement = select(User).where(User.email == credentials.username)
    user = session.exec(statement).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


# ---- PROTEGER ENDPOINTS PARA ADMIN ----
def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
