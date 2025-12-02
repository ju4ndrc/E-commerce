import os

from fastapi import FastAPI,Request

from sqlmodel import select

from models import User, RoleEnum
from .auth.hashing import get_password_hash
from .routers import users, customers, orderd, admin

from app.routers import products
#Async
from contextlib import asynccontextmanager
from db import init_db, async_session
#templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
#super user credentials
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)


    SUPER_EMAIL = os.getenv("SUPERUSER_EMAIL")

    SUPER_EMAIL_PASSWORD = os.getenv("SUPERUSER_PASS")

    SUPER_USERNAME = os.getenv("SUPERUSER_NAME")

    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == SUPER_EMAIL))
        admin_user = result.scalars().first()

        if not admin_user:
            new_admin = User(
                username=SUPER_USERNAME,
                email=SUPER_EMAIL,
                password=get_password_hash(SUPER_EMAIL_PASSWORD),
                role=RoleEnum.ADMIN,
                is_active=True,
            )
            session.add(new_admin)
            await session.commit()
            print(new_admin,"-> was created")
        else:
            print("Already exists")

    yield
app = FastAPI(lifespan=lifespan)

#Templates
templates = Jinja2Templates(directory="templates")

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")



# Rutas y configuración

app.include_router(users.router)

app.include_router(products.router)

app.include_router(customers.router)

app.include_router(orderd.router)

app.include_router(admin.router)

@app.get("/",response_class=HTMLResponse,status_code=200)
async def root(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

