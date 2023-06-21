import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    CustomerContextCreateRequest,
    UpdateCustomerContextRequest,
    GetCustomerContextRequest,
    GetCustomerContextResponse,
)
from repetitor_backend.db.crud import customer_context

logger = logging.getLogger()

router = APIRouter()


@router.post("/customer_context/")
async def create_customer_context(
    new_customer_context: CustomerContextCreateRequest,
) -> UUID:
    """creating a new user context or
    updating the time provided that the combination of three foreign keys already exists in the database.
    створення нового контексту користувача, або оновлення часу при умові, що комбінація трьох зовн.ключів уже є в БД
        Parameters:

    """
    return await customer_context.create(**new_customer_context.dict())


@router.get(
    "/customer_context/",
    response_model=List[GetCustomerContextResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_customer_context(
    id: UUID | None = None,
    customer: UUID = None,
    context_1: UUID = None,
    context_2: UUID = None,
    is_active: bool = True,
    is_key_only: Annotated[bool, Query(description="if only 'id' is needed")] = False,
) -> list:
    """Get list of CustomerContext according of "query" parameter"""
    get_param_customer_context = GetCustomerContextRequest(
        id=id,
        customer=customer,
        context_1=context_1,
        context_2=context_2,
        is_active=is_active,
    )
    results = await customer_context.get(**get_param_customer_context.dict())
    if is_key_only:
        fin_result = [
            {"id": result.id}
            for result in results
            if isinstance(result, tables.CustomerContext)
        ]
    else:
        fin_result = [
            result.to_dict()
            for result in results
            if isinstance(result, tables.CustomerContext)
        ]
    return fin_result


@router.patch("/customer_context/")
async def update_customer_context(
    id: UUID, update_param_customer_context: UpdateCustomerContextRequest
) -> UUID | None:
    """Update CustomerContext according of "query" parameter"""

    return await customer_context.update(id=id, **update_param_customer_context.dict())


@router.delete("/customer_context/")
async def delete_customer_context(id_param: UUID) -> UUID | None:
    """Update CustomerContext according of "query" parameter"""

    return await customer_context.delete(id_param)
