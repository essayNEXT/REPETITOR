__all__ = ["router"]

from fastapi import APIRouter
from repetitor_backend.api.v1.customer.views import router as customers_router
from repetitor_backend.api.v1.type.views import router as type_router
from repetitor_backend.api.v1.item.views import router as item_router
from repetitor_backend.api.v1.context.views import router as context_router
from repetitor_backend.api.v1.customer_context.views import (
    router as customer_context_router,
)

# from repetitor_backend.api.v1.translate.views import router as translate_router

router = APIRouter()

router.include_router(customers_router, tags=["Customers"])
router.include_router(type_router, tags=["Type"])
router.include_router(item_router, tags=["Item"])
router.include_router(context_router, tags=["Context"])
router.include_router(customer_context_router, tags=["Customer context"])
# router.include_router(translate_router, tags=["Translate"])
