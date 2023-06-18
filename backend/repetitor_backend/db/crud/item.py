from uuid import UUID
from typing import Optional, List, Annotated

from fastapi import Query

from repetitor_backend import tables
from repetitor_backend.api.v1.item.serializers import UpdateItemRequest


async def create(text: str, **kwargs) -> UUID:
    """Create new item.

    parameters:

    """

    if not isinstance(text, str):
        raise TypeError(
            f"paremeter 'text' and 'image' for context_type must be only\
str-type, but type(text)={type(text)} "
        )
    elif not len(text) <= 20:
        raise ValueError(f"len(text) must be <= 20, but got len(text)={len(text)}")
    result = await tables.Item.insert(tables.Item(text=text, **kwargs)).returning(
        tables.Item.id
    )
    return result[0]["id"]


async def get(
    id: Optional[UUID] = None,
    author: Optional[int] = None,
    text: Optional[str] = None,
    is_active: Optional[bool] = True,
    context: UUID | None = None,
    image: Annotated[
        str | None, Query(min_length=3, max_length=255)  # , regex=REGEX_PATH)
    ] = None,
    sound: Annotated[
        str | None, Query(min_length=3, max_length=255)  # , regex=REGEX_PATH)
    ] = None,
) -> List[tables.Item]:
    """Get a list of existing items according to match conditions:"""
    query = tables.Item.objects().where(tables.Item.is_active == is_active)
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


async def update(
    id: UUID,
    **update_param: UpdateItemRequest
    # author: Optional[int] = None,
    # is_active: Optional[bool] = True,
    # context: UUID | None = None,
    # text: Annotated[
    #     str | None, Query(min_length=2, max_length=255)
    # ] = None,
    # image: Annotated[
    #     str | None, Query(min_length=3, max_length=255)  # , regex=REGEX_PATH)
    # ] = None,
    # sound: Annotated[
    #     str | None, Query(min_length=3, max_length=255)  # , regex=REGEX_PATH)
    # ] = None,
) -> UUID | None:
    """Update existing record in item.

    parameters:

    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update_item must be UUID-type, but got {type(id)}"
        )
    # kwargs = {}
    # if text is not None:
    #     if not isinstance(text, str):
    #         raise TypeError(
    #             f"parameter 'text' for function update_item must be str-type, but got {type(text)}"
    #         )
    #     # if len(text) > 20:
    #     #     raise ValueError(
    #     #         f"the 'text' parameter must be no more than 20 characters long, received {len(text)}"
    #     #     )
    #     kwargs["text"] = text
    #
    # if image is not None:
    #     if not isinstance(image, str):
    #         raise TypeError(
    #             f"parameter 'image' for function update_item must be str-type, but got {type(image)}"
    #         )
    #     kwargs["image"] = image
    # if sound is not None:
    #     if not isinstance(sound, str):
    #         raise TypeError(
    #             f"parameter 'image' for function update_item must be str-type, but got {type(sound)}"
    #         )
    #     kwargs["sound"] = sound
    # if is_active is not None:
    #     if not isinstance(is_active, bool):
    #         raise TypeError(
    #             f"parameter 'is_active' for function update_item must be bool-type, but got {type(is_active)}"
    #         )
    #     kwargs["is_active"] = is_active
    filtered_param = {k: v for k, v in update_param.items() if v is not None}
    result = (
        await tables.Item.update(filtered_param)
        .where(tables.Item.id == id)
        .returning(tables.Item.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete context_type with context_type.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type. If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_context_type must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
