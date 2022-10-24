from fastapi import APIRouter
from app.config import Settings
from app.api.endpoints import posts
settings = Settings()

api_router = APIRouter(prefix=f"/{settings.url_prefix}/{settings.api_version}")

api_router.include_router(posts.router)
