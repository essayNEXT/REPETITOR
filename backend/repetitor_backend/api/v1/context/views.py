import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    ContextCreateRequest,
    UpdateContextRequest,
    GetContextRequest,
    GetContextResponse,
)
from repetitor_backend.db.crud import context

logger = logging.getLogger()

router = APIRouter()


@router.post("/context/")
async def create_context(new_context: ContextCreateRequest) -> UUID:
    """Create new item.
    Parameters:
        - name: str, max lenght is 50 symbols - the name of the context, required
        - name_short: str, max lenght is 10 symbols - the short name of the context, required
        - context_class: UUID of context, used for ForeignKey links with Context, required
        - description: str, max lenght is 255 symbols - context description, required
        - is_active: bool = True
    Return:
    - Item.id: UUID - primary key for new item record - UUID type
    """
    return await context.create(**new_context.dict())


@router.get(
    "/context/",
    response_model=List[GetContextResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_context(
    id: UUID | None = None,
    name: Annotated[str, Query(min_length=1, max_length=50)] = None,
    name_short: Annotated[str, Query(min_length=1, max_length=10)] = None,
    context_class: UUID = None,
    description: Annotated[str, Query(min_length=2, max_length=255)] = None,
    is_active: bool = True,
    is_key_only: Annotated[bool, Query(description="if only 'id' is needed")] = False,
) -> list:
    """Get a list of existing item according to match conditions:
        Parameters:
        - id: UUID of item
        - name: str, max lenght is 50 symbols - the name of the context
        - name_short: str, max lenght is 10 symbols - the short name of the context
        - context_class: UUID of context, used for ForeignKey links with Context
        - description: str, max lenght is 255 symbols - context description
        - is_active: bool = True
        - is_key_only: bool - as a result, return:
            - only the ID of the item object;
            - return all object parameters
    Return:
    - List that contains the results of the query
    """
    get_param_context = GetContextRequest(
        id=id,
        name=name,
        name_short=name_short,
        context_class=context_class,
        description=description,
        is_active=is_active,
    )
    results = await context.get(**get_param_context.dict())
    if is_key_only:
        fin_result = [
            {"id": result.id}
            for result in results
            if isinstance(result, tables.Context)
        ]
    else:
        fin_result = [
            result.to_dict() for result in results if isinstance(result, tables.Context)
        ]
    return fin_result


@router.patch("/context/")
async def update_context(
    id: UUID, update_param_context: UpdateContextRequest
) -> UUID | None:
    """Update existing record in customer context.

    parameters:
        - id: UUID of item
        - name: str, max lenght is 50 symbols - the name of the context
        - name_short: str, max lenght is 10 symbols - the short name of the context
        - context_class: UUID of context, used for ForeignKey links with Context
        - description: str, max lenght is 255 symbols - context description
        - is_active: bool = True
    Return:
    - CustomerContext.id: UUID - primary key for new customer context record - UUID type
    - If there is no record with this id, it returns None
    """

    return await context.update(id=id, **update_param_context.dict())


@router.delete("/context/")
async def delete_context(id_param: UUID) -> UUID | None:
    """Delete context with context.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await context.delete(id_param)
