import os
from fastapi.security import OAuth2PasswordBearer
from models import User
from db import SessionDep
from hash import verify_password

from dotenv import load_dotenv


load_dotenv()



SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db,username:str):
    user_db = db.get_user(username)
    if user_db:
        return User(**user_db)

def authenticate_user(session:SessionDep,username:str,password:str):
    user = get_user(session,username)
    if not user or not verify_password(password,user.password):
        return None
    return user

