from fastapi import FastAPI

from app.api.router import api_router
from app.config import VERSION

app = FastAPI(
    title="Facebook App",
    description="Backend REST API service for the mobile app",
    version=VERSION,
)

app.include_router(api_router)
