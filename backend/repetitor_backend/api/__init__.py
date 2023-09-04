from fastapi import APIRouter

from repetitor_backend.api.v1 import router as v1_router
from repetitor_help.api.v1 import router as v1_help_router

router = APIRouter()

router.include_router(v1_router, prefix="/v1", tags=["api/v1"])
router.include_router(v1_help_router, prefix="/v1", tags=["api/v1"])
