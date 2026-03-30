from fastapi import APIRouter

from app.api.v1.parents import router as parent_router
from app.api.v1.providers import router as provider_router
from app.api.v1.pets import router as pet_router

api_router = APIRouter()

api_router.include_router(parent_router, prefix="/parents", tags=["Parents"])
api_router.include_router(provider_router, prefix="/providers", tags=["Providers"])
api_router.include_router(pet_router, prefix="/pets", tags=["Pets"])