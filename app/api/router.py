from fastapi import APIRouter

from app.api.routes import aluno

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(aluno.router)
