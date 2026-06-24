from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401 — registra os models na Base
from app.api.router import api_router
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="SIGMA",
    description="Sistema de gestão acadêmica — API de alunos.",
    version="1.0.0",
)

app.include_router(api_router)
