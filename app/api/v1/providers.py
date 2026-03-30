from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def provider_ping():
    return {"message": "Providers route is working"}