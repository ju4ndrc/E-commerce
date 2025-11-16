
from fastapi import FastAPI

from .routers import users, customers, orderd

from app.routers import prodcuts
from fastapi.staticfiles import StaticFiles
#Async
from contextlib import asynccontextmanager
from db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    yield
app = FastAPI(lifespan=lifespan)


# -----------------------------
# Rutas y configuración
# -----------------------------
app.include_router(users.router)

app.include_router(prodcuts.router)

app.include_router(customers.router)

app.include_router(orderd.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return {"Hello": "World"}


