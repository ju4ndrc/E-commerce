
from fastapi import FastAPI,Request

from .routers import users, customers, orderd

from app.routers import prodcuts
#Async
from contextlib import asynccontextmanager
from db import init_db
#templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    yield
app = FastAPI(lifespan=lifespan)

#Templates
templates = Jinja2Templates(directory="templates")

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")



# Rutas y configuración

app.include_router(users.router)

app.include_router(prodcuts.router)

app.include_router(customers.router)

app.include_router(orderd.router)



@app.get("/",response_class=HTMLResponse,status_code=200)
async def root(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})


