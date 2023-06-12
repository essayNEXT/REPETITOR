__all__ = ["router"]

from fastapi import APIRouter
from repetitor_backend.api.v1.customer.views import router as customers_router
from repetitor_backend.api.v1.type.views import router as type_router


router = APIRouter()

router.include_router(customers_router,
                      tags=["Customers"])
router.include_router(type_router,
                      tags=["Type"])
