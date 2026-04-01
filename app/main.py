from fastapi import FastAPI
from app.api.v1.router import api_router 
from app.core.exception_handlers import register_exception_handlers
from app.db import models

app = FastAPI(
    title="Petssador Backend API",
    version="1.0.0",
    description="Backend API for Petssador platform",
)

register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}