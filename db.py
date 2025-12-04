from fastapi import FastAPI
from fastapi import Depends
from typing import Annotated
from sqlmodel import SQLModel
#async
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine, AsyncEngine
from dotenv import load_dotenv


# sqlite db

#
# sqlite_name = "db.sqlite3"
# sqlite_url = f"sqlite:///{sqlite_name}"
#
#
# engine = create_engine(sqlite_url)
#
# def create_all_tables(app:FastAPI):
#     SQLModel.metadata.create_all(engine)
#     yield
#
# def get_session() -> Session:
#     with Session(engine) as session:
#         yield session
#
# SessionDep = Annotated [Session,Depends(get_session)]

# async db
load_dotenv()

DB_NAME = os.getenv("POSTGRESQL_ADDON_DB")
DB_USER = os.getenv("POSTGRESQL_ADDON_USER")
DB_PASSWORD = os.getenv("POSTGRESQL_ADDON_PASSWORD")
DB_HOST = os.getenv("POSTGRESQL_ADDON_HOST")
DB_PORT = os.getenv("POSTGRESQL_ADDON_PORT")

CLEVER_URL = (f"postgresql+asyncpg://{DB_USER}.efkhgpbtnzebatbsmfqv:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


engine_clever: AsyncEngine = create_async_engine(
    CLEVER_URL,
    echo=True,
)
async_session = sessionmaker(engine_clever, expire_on_commit=False, class_=AsyncSession)

async def init_db(app: FastAPI):
    async with engine_clever.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session_clever():
    async with async_session() as session:
        yield session

SessionDep = Annotated[async_session, Depends(get_session_clever)]

