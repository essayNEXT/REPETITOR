import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    ItemRelationCreateRequest,
    UpdateItemRelationRequest,
    GetItemRelationRequest,
    GetItemRelationResponse,
)
from repetitor_backend.db.crud import item_relation

logger = logging.getLogger()

router = APIRouter()


@router.post("/item_relation/")
async def create_item_relation(
    new_item_relation: ItemRelationCreateRequest,
) -> UUID | str:
    """
    Create new customer context.

    Parameters:
    - customer: UUID of customer, used for ForeignKey links with Customer, required
    - context_1: UUID of context, used for ForeignKey links with Context, required
    - context_2: UUID of context, used for ForeignKey links with Context, required

    Return:
    - ItemRelation.id: UUID - primary key for new customer context record - UUID type
    - str - error message in case of invalid foreign keys
    """
    return await item_relation.create(**new_item_relation.dict())


@router.get(
    "/item_relation/",
    response_model=List[GetItemRelationResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_item_relation(
    id: UUID | None = None,
    author: UUID = None,
    explanation: UUID = None,
    type: UUID = None,
    is_active: bool = True,
    explanation__description: str | None = None,
    type__name: Annotated[str | None, Query(min_length=2, max_length=30)] = None,
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
    get_param_item_relation = GetItemRelationRequest(
        id=id,
        author=author,
        explanation=explanation,
        type=type,
        explanation__description=explanation__description,
        type__name=type__name,
        is_active=is_active,
    )
    results = await item_relation.get(**get_param_item_relation.dict())
    fin_result = [
        result.to_dict()
        for result in results
        if isinstance(result, tables.ItemRelation)
    ]
    return fin_result


@router.patch("/item_relation/")
async def update_item_relation(
    id: UUID, update_param_item_relation: UpdateItemRelationRequest
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
    - ItemRelation.id: UUID - primary key for new customer context record - UUID type
    - If there is no record with this id, it returns None
    """

    return await item_relation.update(id=id, **update_param_item_relation.dict())


@router.delete("/item_relation/")
async def delete_item_relation(id_param: UUID) -> UUID | None:
    """
    Delete item_relation with item_relation.id == id.

    Parameter:
    - id - UUID.

    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await item_relation.delete(id_param)
