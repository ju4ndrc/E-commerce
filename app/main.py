from fastapi import FastAPI, Request, status

from db import create_all_tables, engine, SessionDep
from .routers import users, customers, orderd
from app.auth import auth_router
from app.routers import prodcuts
from fastapi.staticfiles import StaticFiles


app = FastAPI(lifespan=create_all_tables)


# -----------------------------
# Rutas y configuración
# -----------------------------
app.include_router(users.router)
app.include_router(auth_router.router)
app.include_router(prodcuts.router)

app.include_router(customers.router)

app.include_router(orderd.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return {"Hello": "World"}


