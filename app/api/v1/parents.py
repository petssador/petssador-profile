from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def parent_ping():
    return {"message": "Parents route is working"}