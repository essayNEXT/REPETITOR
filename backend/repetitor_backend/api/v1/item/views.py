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
async def create_item(new_item: ItemCreateRequest) -> UUID:
    """Create a new type of customer.

    Parameters:
    - name: str, max lenght is 50 symbols, required
    - describe: str, max lenght is 200 symbols, required
    """
    return await item.create(**new_item.dict())


@router.get(
    "/items/",
    response_model=List[ItemResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_item(
    text: str,
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
    """Get list of Item according of "query" parameter"""
    results = await item.get(
        id=id,
        author=author,
        text=text,
        context=context,
        sound=sound,
        image=image,
        is_active=is_active,
    )
    1 == 1
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
    """Update Item according of "query" parameter"""

    results = await item.update(**update_item.dict())
    1 == 1
    return results


@router.delete("/items/")
async def update_item(id: UUID) -> UUID | None:
    """Update Item according of "query" parameter"""

    return await item.delete(id)
