from uuid import UUID
from typing import Optional, List, Annotated

from asyncpg import ForeignKeyViolationError
from fastapi import Query

from repetitor_backend import tables
from repetitor_backend.api.v1.item.serializers import UpdateItemRequest


async def create(text: str, **kwargs) -> UUID | str:
    """Create new item.
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

    if not isinstance(text, str):
        raise TypeError(
            f"paremeter 'text' for context_type must be only str-type, but type(text)={type(text)} "
        )
    elif not len(text) <= 20:
        raise ValueError(f"len(text) must be <= 20, but got len(text)={len(text)}")
    kwargs["text"] = text
    check_exists = await get(**kwargs)
    if check_exists:  # якщо існує  такий запис
        return f"an object with such parameters already exists id={check_exists[0].id}  is_active={check_exists[0].is_active} "
        raise TypeError(
            f"an object with such parameters already exists {check_exists[0].id}"
        )
    try:
        result = await tables.Item.insert(tables.Item(**kwargs)).returning(
            tables.Item.id
        )
    except ForeignKeyViolationError as e:
        return str(e)
    return result[0]["id"]


async def get(
    id: UUID | None = None,
    author: UUID | None = None,
    text: Optional[str] = None,
    is_active: Optional[bool] = None,
    context: UUID | None = None,
    image: Annotated[
        str | None, Query(min_length=3, max_length=255)  # , regex=REGEX_PATH)
    ] = None,
    sound: Annotated[
        str | None, Query(min_length=3, max_length=255)  # , regex=REGEX_PATH)
    ] = None,
) -> List[tables.Item]:
    """Get a list of existing item according to match conditions:
        Parameters:
        - id: UUID of item
        - text: str, max lenght is 255 symbols - data description
        - image: str, max lenght is 255 symbols - link to associative picture
        - sound: str, max lenght is 255 symbols - link to associative sound
        - author: UUID of customer, used for ForeignKey links with Customer
        - context: UUID of context, used for ForeignKey links with Context

    Return:
    - List that contains the results of the query
    """
    query = tables.Item.objects()
    if is_active:
        query = query.where(tables.Item.is_active == is_active)
    if id:
        query = query.where(tables.Item.id == id)
    if author:
        query = query.where(tables.Item.author == author)
    if context:
        query = query.where(tables.Item.context == context)
    if image:
        query = query.where(tables.Item.image == image)
    if sound:
        query = query.where(tables.Item.sound == sound)
    if text:
        query = query.where(tables.Item.text.like("%" + text + "%"))
    result = await query
    return result


async def update(id: UUID, **update_param: UpdateItemRequest) -> UUID | None:
    """Update existing record in customer context.

    parameters:
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
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update_item must be UUID-type, but got {type(id)}"
        )
    filtered_param = {k: v for k, v in update_param.items() if v is not None}
    result = (
        await tables.Item.update(filtered_param)
        .where(tables.Item.id == id)
        .returning(tables.Item.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete item with item.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_item must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
