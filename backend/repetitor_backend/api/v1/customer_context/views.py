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
    """
    Create new customer context.

    Parameters:
    - customer: UUID of customer, used for ForeignKey links with Customer, required
    - context_1: UUID of context, used for ForeignKey links with Context, required
    - context_2: UUID of context, used for ForeignKey links with Context, required
    - last_date: customer context creation time, UTС zone
    - is_active: bool = True

    Return:
    - CustomerContext.id: UUID - primary key for new customer context record - UUID type
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
    """
    Get a list of existing customer context according to match conditions:

    Parameters:
    - id: UUID of customer context
    - customer: UUID of customer, used for ForeignKey links with Customer
    - context_1: UUID of context, used for ForeignKey links with Context
    - context_2: UUID of context, used for ForeignKey links with Context
    - last_date: customer context creation/update time, UTС zone
    - is_active: bool = True

    Return:
    - List that contains the results of the query
    """
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
    """
    Update existing record in customer context.

    Parameters:
    - id: UUID of customer context, required
    - customer: UUID of customer, used for ForeignKey links with Customer
    - context_1: UUID of context, used for ForeignKey links with Context
    - context_2: UUID of context, used for ForeignKey links with Context
    - last_date: customer context creation/update time, UTС zone
    - is_active: bool = True

    Return:
    - CustomerContext.id: UUID - primary key for new customer context record - UUID type
    - If there is no record with this id, it returns None
    """

    return await customer_context.update(id=id, **update_param_customer_context.dict())


@router.delete("/customer_context/")
async def delete_customer_context(id_param: UUID) -> UUID | None:
    """
    Delete customer_context with customer_context.id == id.

    Parameter:
    - id - UUID.

    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await customer_context.delete(id_param)
