import uuid
from http.client import responses

from fastapi import APIRouter, status, HTTPException, Query, Depends

from app.auth.auth_router import admin_required
from app.auth.hash import hash_password

from sqlmodel import select


from db import SessionDep
from models import User,UserBase,CreateUser,UpdateUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, )
async def createUser(user_data: CreateUser, session: SessionDep):
    hashed_pw = hash_password(user_data.password)
    user = User.model_validate({
        **user_data.model_dump(),
        "password": hashed_pw
    })
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def soft_delete_user(user_id: uuid.UUID, session: SessionDep, user : User = Depends(admin_required)):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_db.is_active:
        raise HTTPException(status_code=400, detail="User already inactive")

    user_db.is_active = False
    session.add(user_db)
    session.commit()
    return {"message": "User deactivated successfully", "user_id": str(user_id)}
@router.patch("/reactivate/{user_id}", response_model=User)
async def reactivate_user(user_id: uuid.UUID, session: SessionDep, user : User = Depends(admin_required)):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_db.is_active = True
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db
@router.get("/",response_model=list[User])
async def show_users(session:SessionDep, user : User = Depends(admin_required)):
    response = session.exec(select(User)).all()
    return response
@router.get("/active", response_model=list[User])
async def get_users(session: SessionDep, user : User = Depends(admin_required)):
    users = session.exec(select(User).where(User.is_active == True)).all()
    return users

@router.patch("/updateUser/{user_id}",response_model=User,status_code= status.HTTP_201_CREATED)
async def update_user( user_id: uuid.UUID, user_data:UpdateUser, session:SessionDep, user : User = Depends(admin_required) ):
    user_db = session.get(User, user_id)

    if not user_db:

        raise HTTPException(status_code=404, detail="We can not find, this user")

    user_data_dict = user_data.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data_dict)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db