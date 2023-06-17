import logging
from uuid import UUID
from .serializers import CustomerCreateRequest, CustomerUpdateRequest
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
        tlg_user_name=new_customer.tlg_user_name,
        tlg_last_name=new_customer.tlg_last_name,
        native_language=new_customer.native_language,
        first_name=new_customer.first_name,
        last_name=new_customer.last_name,
        email=new_customer.email,
    )


@router.put("/customer")
async def update_customer(update_customer: CustomerUpdateRequest):
    return await customer.update_customer(
        id=update_customer.id,
        customer_class=update_customer.customer_class,
        tlg_user_id=update_customer.tlg_user_id,
        tlg_language=update_customer.tlg_language,
        tlg_first_name=update_customer.tlg_first_name,
        tlg_user_name=update_customer.tlg_user_name,
        tlg_last_name=update_customer.tlg_last_name,
        native_language=update_customer.native_language,
        first_name=update_customer.first_name,
        last_name=update_customer.last_name,
        email=update_customer.email,
        is_active=update_customer.is_active,
    )


@router.delete("/customer")
async def delete_customer(id: UUID):
    return await customer.update_customer(id=id, is_active=False)
