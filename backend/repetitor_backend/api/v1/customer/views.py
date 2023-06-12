import logging
from uuid import UUID


from fastapi import APIRouter
from repetitor_backend.db.crud import customer

logger = logging.getLogger()

router = APIRouter()


@router.get("/customer")
async def get_customer(
        customer_id: UUID | int
):
    result = await customer.get_customer(
        customer_id=customer_id
    )
    return result
