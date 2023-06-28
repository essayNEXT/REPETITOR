import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter

from .serializers import (
    CustomerTypeCreateRequest,
    CustomerTypeResponse,
    ContextTypeCreateRequest,
    ContextTypeResponse,
)
from repetitor_backend.db.crud import contexttype, customertype

logger = logging.getLogger()

router = APIRouter()


@router.post("/type/customer/")
async def create_customer_type(new_customer_type: CustomerTypeCreateRequest) -> UUID:
    """Create a new type of customer.

    Parameters:
    - name: str, max lenght is 50 symbols, required
    - describe: str, max lenght is 200 symbols, required
    """
    return await customertype.create_new_customer_type(
        name=new_customer_type.name, description=new_customer_type.description
    )


@router.get("/type/customer/")
async def get_customer_type(
    id: UUID | None = None,
    name: str | None = None,
    description: str | None = None,
    is_active: bool = True,
) -> List[CustomerTypeResponse]:
    """Get list of Customer Type according of "query" parameter.

    id: UUID, corresponds to the parameter tables.CustomerType.id
    name: str, corresponds to the parameter tables.CustomerType.name
    description: str, corresponds to the parameter tables.CustomerType.description
    is_active: bool, corresponds to the parameter tables.CustomerType.is_active

    Returns a list that contains the results of the query, serialized to
    the CustomerTypeResponce type, constructed as follows:
    SELECT *
    FROM customer_type
    WHERE
            customer_type.id = id
        AND customer_type.name = name
        AND customer_type.description LIKE '%description%'
        AND customer_type.is_active = is_active;

    if some parameter is None (as id, name, description) - the corresponding line
    in the request is simply missing
    """
    results = await customertype.get_customer_type(
        id=id, name=name, description=description, is_active=is_active
    )
    return [CustomerTypeResponse.from_DB_model(db_model=result) for result in results]


@router.post("/type/context/")
async def create_context_type(new_context_type: ContextTypeCreateRequest) -> UUID:
    """Create a new type of context.

    Parameters:
    - name: str, max lenght is 50 symbols, required
    - describe: str, max lenght is 200 symbols, required
    """
    return await contexttype.create(
        name=new_context_type.name, description=new_context_type.description
    )


@router.get("/type/context/")
async def get_context_type(
    id: UUID | None = None,
    name: str | None = None,
    description: str | None = None,
    is_active: bool = True,
) -> List[ContextTypeResponse]:
    """Get list of Context Type according of "query" parameter.

    id: UUID, corresponds to the parameter tables.ContextType.id
    name: str, corresponds to the parameter tables.ContextType.name
    description: str, corresponds to the parameter tables.ContextType.description
    is_active: bool, corresponds to the parameter tables.ContextType.is_active

    Returns a list that contains the results of the query, serialized to
    the CustomerTypeResponce type, constructed as follows:
    SELECT *
    FROM customer_type
    WHERE
            customer_type.id = id
        AND customer_type.name = name
        AND customer_type.describe LIKE '%describe%'
        AND customer_type.is_active = is_active;

    if some parameter is None (as id, name, describe) - the corresponding line
    in the request is simply missing
    """
    results = await contexttype.get(
        id=id, name=name, description=description, is_active=is_active
    )
    return [ContextTypeResponse.from_DB_model(db_model=result) for result in results]
