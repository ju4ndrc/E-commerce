import uuid

from fastapi import APIRouter, status, HTTPException,Request

from sqlmodel import select


from db import SessionDep
from models import User,CreateUser,UpdateUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, )
async def createUser(request:Request,user_data: CreateUser, session: SessionDep):
    user = User.model_validate(user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def soft_delete_user(user_id: uuid.UUID, session: SessionDep):
    user_db = await session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_db.is_active:
        raise HTTPException(status_code=400, detail="User already inactive")

    user_db.is_active = False
    session.add(user_db)
    await session.commit()
    return {"message": "User deactivated successfully", "user_id": str(user_id)}
@router.patch("/reactivate/{user_id}", response_model=User)
async def reactivate_user(user_id: uuid.UUID, session: SessionDep):
    user_db = await session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_db.is_active = True
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db
@router.get("/",response_model=list[User])
async def show_users(session:SessionDep):
    query : select(User)
    response = await session.execute(select(User))
    users = response.scalars().all()
    return users
@router.get("/active", response_model=list[User])
async def get_users(session: SessionDep):
    result = await session.execute(select(User).where(User.is_active == True))
    users = result.scalars().all()
    return users
@router.get("/{user_id}", response_model=User)
async def get_user(request:Request,user_id: uuid.UUID, session: SessionDep):
    user_db = await session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db
@router.patch("/updateUser/{user_id}",response_model=User,status_code= status.HTTP_201_CREATED)
async def update_user( user_id: uuid.UUID, user_data:UpdateUser, session:SessionDep ):
    user_db = await session.get(User, user_id)

    if not user_db:

        raise HTTPException(status_code=404, detail="We can not find, this user")

    user_data_dict = user_data.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data_dict)
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db