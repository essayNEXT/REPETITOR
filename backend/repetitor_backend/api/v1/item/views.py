import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend import tables
from .serializers import (
    ItemCreateRequest,
    ItemResponse,
    REGEX_PATH,
    UpdateItemRequest,
)
from repetitor_backend.db.crud import item

logger = logging.getLogger()

router = APIRouter()


@router.post("/items/")
async def create_item(new_item: ItemCreateRequest) -> UUID | str:
    """
    Create new item.

    Parameters:
    - text: str, max lenght is 255 symbols - data description, required
    - image: str, max lenght is 255 symbols - link to associative picture
    - sound: str, max lenght is 255 symbols - link to associative sound
    - author: UUID of customer, used for ForeignKey links with Customer, required
    - context: UUID of context, used for ForeignKey links with Context, required

    Return:
    - Item.id: UUID - primary key for new item record - UUID type
    - str - error message in case of invalid foreign keys
    """
    return await item.create(**new_item.dict())


@router.get(
    "/items/",
    response_model=List[ItemResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_item(
    text: str | None = None,
    id: UUID | None = None,
    image: Annotated[
        str | None, Query(min_length=3, max_length=255, regex=REGEX_PATH)
    ] = None,
    sound: Annotated[
        str | None, Query(min_length=3, max_length=255, regex=REGEX_PATH)
    ] = None,
    author: UUID | None = None,
    context: UUID | None = None,
    is_active: bool = True,
    is_key_only: Annotated[
        bool, Query(description="if only 'id' is needed")
    ] = False,  # якщо потрібно тільки самі
) -> list:
    """
    Get a list of existing item according to match conditions:

    Parameters:
    - id: UUID of item
    - text: str, max lenght is 255 symbols - data description
    - image: str, max lenght is 255 symbols - link to associative picture
    - sound: str, max lenght is 255 symbols - link to associative sound
    - author: UUID of customer, used for ForeignKey links with Customer
    - context: UUID of context, used for ForeignKey links with Context
    - is_key_only: bool - as a result, return:
        - only the ID of the item object;
        - return all object parameters

    Return:
    - List that contains the results of the query
    """
    results = await item.get(
        id=id,
        author=author,
        text=text,
        context=context,
        sound=sound,
        image=image,
        is_active=is_active,
    )
    if is_key_only:
        fin_result = [
            {"id": result.id} for result in results if isinstance(result, tables.Item)
        ]
    else:
        fin_result = [
            result.to_dict() for result in results if isinstance(result, tables.Item)
        ]
    return fin_result


@router.patch("/items/")
async def update_item(update_item: UpdateItemRequest) -> UUID | None:
    """
    Update existing record in customer context.

    Parameters:
    - id: UUID of customer context, required
    - text: str, max lenght is 255 symbols - data description
    - image: str, max lenght is 255 symbols - link to associative picture
    - sound: str, max lenght is 255 symbols - link to associative sound
    - author: UUID of customer, used for ForeignKey links with Customer
    - context: UUID of context, used for ForeignKey links with Context

    Return:
    - CustomerContext.id: UUID - primary key for new customer context record - UUID type
    - If there is no record with this id, it returns None
    """

    return await item.update(**update_item.dict())


@router.delete("/items/")
async def delete_item(id: UUID) -> UUID | None:
    """
    Delete item with item.id == id.

    Parameter:
    - id - UUID.

    Result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await item.delete(id)
