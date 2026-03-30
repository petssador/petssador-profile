from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def pet_ping():
    return {"message": "Pets route is working"}