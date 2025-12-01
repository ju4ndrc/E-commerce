import uuid

from typing import Optional

from fastapi import APIRouter, status, HTTPException,Request,Form,File,UploadFile
from sqlmodel import select
from starlette.responses import RedirectResponse

from db import SessionDep
from models import User,UpdateUser,CreateUser
from supa_impt.supa_bucket import upload_to_bucket
#Templates response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router = APIRouter(prefix="/users", tags=["Users"])
templates = Jinja2Templates(directory="templates")

@router.get("/register",response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, )
async def create_user(
        request:Request,
        session: SessionDep,
        username:str = Form(...),
        password:str = Form(...),
        email:str = Form(...),
        status:bool = Form(True),
        img:Optional[UploadFile] = File(None)
        ):
    img_url = None
    if img:
        try:
            img_url = await upload_to_bucket(img)

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

    return RedirectResponse(url="/users",status_code=302)
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
@router.get("/",response_class=HTMLResponse)
async def show_users(request:Request,session:SessionDep):
    response = await session.execute(select(User))
    users = response.scalars().all()
    return templates.TemplateResponse("users/show_users.html",
                                      {"request": request, "users": users})
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

@router.get("/update/{user_id}", response_class=HTMLResponse ,status_code=status.HTTP_200_OK)
async def show_user(request:Request, session: SessionDep, user_id: uuid.UUID,):
    user = await session.get(User, user_id)
    await session.refresh(user)
    return templates.TemplateResponse("users/update_user.html",{"request": request, "user": user})
@router.post("/update/{user_id}",response_model=User,status_code= status.HTTP_201_CREATED)
async def update_user(
        request:Request,
        session:SessionDep ,
        user_id: uuid.UUID,

        username:Optional[str] = Form(None),
        password:Optional[str] = Form(None),
        email:Optional[str] = Form(None),
        status:Optional[bool] = Form(True),
        img:Optional[UploadFile] = File(None)):


    user_db = await session.get(User, user_id)


    if not user_db:

        raise HTTPException(status_code=404, detail="We can not find, this user")

    if username:
        user_db.username = username
    if password:
        user_db.password = password
    if email:
        user_db.email = email
    if status is not None:
        user_db.status = status

    if img and img.filename:
        img_url = await upload_to_bucket(img)
        user_db.img = img_url

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return RedirectResponse(url="/users/",status_code=302)
