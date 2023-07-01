import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    RightAnswItemCreateRequest,
    UpdateRightAnswItemRequest,
    GetRightAnswItemRequest,
    GetRightAnswItemResponse,
)
from repetitor_backend.db.crud import right_answ_item

logger = logging.getLogger()

router = APIRouter()


@router.post("/right_answ_item/")
async def create_right_answ_item(
    new_right_answ_item: RightAnswItemCreateRequest,
) -> UUID | str:
    """
    Create new customer context.

    Parameters:
    - customer: UUID of customer, used for ForeignKey links with Customer, required
    - context_1: UUID of context, used for ForeignKey links with Context, required
    - context_2: UUID of context, used for ForeignKey links with Context, required

    Return:
    - RightAnswItem.id: UUID - primary key for new customer context record - UUID type
    - str - error message in case of invalid foreign keys
    """
    return await right_answ_item.create(**new_right_answ_item.dict())


@router.get(
    "/right_answ_item/",
    response_model=List[GetRightAnswItemResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_right_answ_item(
    id: UUID | None = None,
    relation: UUID = None,
    item: UUID = None,
    is_active: bool = True,
    item__author: UUID | None = None,
    item__context__name_short: Annotated[
        str | None, Query(min_length=2, max_length=10)
    ] = None,
    item__text: Annotated[str | None, Query(min_length=2, max_length=255)] = None,
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
    get_param_right_answ_item = GetRightAnswItemRequest(
        id=id,
        relation=relation,
        item=item,
        item__author=item__author,
        item__context__name_short=item__context__name_short,
        item__text=item__text,
        is_active=is_active,
    )
    results = await right_answ_item.get(**get_param_right_answ_item.dict())
    fin_result = [
        result.to_dict()
        for result in results
        if isinstance(result, tables.RightAnswItem)
    ]
    return fin_result


@router.patch("/right_answ_item/")
async def update_right_answ_item(
    id: UUID, update_param_right_answ_item: UpdateRightAnswItemRequest
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
    - RightAnswItem.id: UUID - primary key for new customer context record - UUID type
    - If there is no record with this id, it returns None
    """

    return await right_answ_item.update(id=id, **update_param_right_answ_item.dict())


@router.delete("/right_answ_item/")
async def delete_right_answ_item(id_param: UUID) -> UUID | None:
    """
    Delete right_answ_item with right_answ_item.id == id.

    Parameter:
    - id - UUID.

    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await right_answ_item.delete(id_param)
