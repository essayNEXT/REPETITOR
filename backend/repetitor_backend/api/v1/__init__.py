__all__ = ["router"]

from fastapi import APIRouter
from repetitor_backend.api.v1.users.views import router as users_router


router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
