import logging
from uuid import UUID
from .serializers import CustomerCreateRequest

from fastapi import APIRouter
from repetitor_backend.db.crud import customer

logger = logging.getLogger()

router = APIRouter()


@router.get("/customer")
async def get_customer(customer_id: UUID | int):
    result = await customer.get_customer(customer_id=customer_id)
    return result


@router.post("/customer")
async def create_customer(new_customer: CustomerCreateRequest):
    return await customer.create_new_customer(
        customer_class=new_customer.customer_class,
        tlg_user_id=new_customer.tlg_user_id,
        tlg_language=new_customer.tlg_language,
        tlg_first_name=new_customer.tlg_first_name,
    )
