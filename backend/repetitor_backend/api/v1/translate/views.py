import logging
from repetitor_backend.external_api.microsoft import translate, translate_lng
from fastapi import APIRouter

logger = logging.getLogger()

router = APIRouter()


@router.get("/translate/ms_lng_list/")
async def ms_lng_list(int_lng: str = "en") -> list:
    """Отримує список мов, які зараз підтримуються операціями Перекладача."""
    from repetitor_backend.app import app

    result = await translate_lng(session=app.session, interface_lng=int_lng)
    return list(result)


@router.get("/translate/ms_translate/")
async def ms_translate(
    src_lng: str = "uk", trg_lng: str = "en", text: str = "додати"
) -> str:
    """
    The function returns the translation of the entered text, in addition,
    it compares the resulting translation with:
    1. by reverse translation or
    2. with the translation "auto-detecting input language"
        (additional option, not used yet)
       and decides on the correctness of the translation.
    Used Microsoft Azure Cognitive Services Translator REST APIs

    :param source_lang: language from which the translation is carried out
    :param target_lang: language into which the translation is carried out
    :param text: text to be translated
    :return: if the translation is correct, then returns the translation of the input text
    """

    from repetitor_backend.app import app

    result = await translate(app.session, src_lng, trg_lng, text)
    return result


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
from repetitor_backend.db.crud import item, question


# logger = logging.getLogger()
#
# router = APIRouter()


@router.post("/translate/")
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
    "/translate/",
    # response_model=List[ItemResponse],
    # response_model_exclude_none=True,
    # response_model_exclude={"is_active"},
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
    context: UUID | str | None = None,
    context_2: UUID | str | None = None,
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
    results = await question.get(
        id=id,
        author=author,
        text=text,
        context=context,
        context_2=context_2,
        sound=sound,
        image=image,
        is_active=is_active,
    )
    # if is_key_only:
    #     fin_result = [
    #         {"id": result.id}
    #         for result in results
    #         if isinstance(result, tables.Question)
    #     ]
    # else:
    #     fin_result = [
    #         result.to_dict()
    #         for result in results
    #         if isinstance(result, tables.Question)
    #     ]
    fin_result = results
    return fin_result


@router.patch("/translate/")
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


@router.delete("/translate/")
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
