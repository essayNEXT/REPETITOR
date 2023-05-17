from fastapi import APIRouter

from repetitor_backend.api.v1 import router as v1_router

router = APIRouter()

router.include_router(v1_router, prefix="/v1", tags=["api/v1"])
