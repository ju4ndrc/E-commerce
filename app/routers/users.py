import uuid

from typing import Optional

from fastapi import APIRouter, status, HTTPException,Request,Form,File,UploadFile
from sqlmodel import select
from db import SessionDep
from models import User,UpdateUser,CreateUser
from supa_impt.supa_bucket import upload_supabase_bucket
#Templates response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router = APIRouter(prefix="/users", tags=["Users"])
templates = Jinja2Templates(directory="templates")
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, )
async def createUser(
        request:Request,
        session: SessionDep,
        username:str = Form(...),
        password:str = Form(...),
        email:str = Form(...),
        status:bool = Form(True),
        img:Optional[UploadFile] = File(...)
        ):
    img_url = None
    if img:
        try:
            img_url = await upload_supabase_bucket(img)
            print("img is in the bucket")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    try:
        new_user = CreateUser(username=username, password=password, email=email,status=status, img=img_url)
        user = User.model_validate(new_user)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
async def show_users(request:Request,session:SessionDep):
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