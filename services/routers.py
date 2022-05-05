from fastapi import APIRouter

from services.test.routers import test_router
from settings import Settings

settings = Settings()

services_router = APIRouter(prefix='/services')

services_router.include_router(router=test_router)


