__all__ = ["router"]

from fastapi import APIRouter
from repetitor_help.api.v1.help.views import router as help_router


router = APIRouter()

router.include_router(help_router, tags=["Help"])
