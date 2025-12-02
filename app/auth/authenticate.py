import os
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from models import User
from db import SessionDep
from app.auth.hashing import verify_password

from dotenv import load_dotenv


load_dotenv()



SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_user(session:SessionDep,username:str):
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.scalars().first()

async def authenticate_user(session:SessionDep,username:str,password:str):
    user = await get_user(session,username)
    if not user or not verify_password(password,user.password):
        return None
    return user

