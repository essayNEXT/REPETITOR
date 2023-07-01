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
from repetitor_backend.db.crud import item, question, right_answ_item


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
    item__text: str,
    item__author: UUID| None,
    item__context__name_short: Annotated[str | None, Query(min_length=2, max_length=10)],
    item__context__name_short_2: Annotated[str| None, Query(min_length=2, max_length=10)],
    is_active: bool = True,
) -> list:
    """
    Get a list of existing item according to match conditions:

    Parameters:
    - id: UUID of item
    - item__text: str, max lenght is 255 symbols - data description
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

    result = await question.get(
        item__author=item__author,
        item__text=item__text,
        item__context__name_short=item__context__name_short,
        is_active=is_active,
    )

    if not result:
        return [{"status": 404, "step": 1}]
    uuid_relation: UUID | None = (
        result[0].relation if result else None
    )  # None = нема такого слова, треба створювати

    result_2 = await right_answ_item.get(
        item__author=item__author,
        relation=uuid_relation,
        item__context__name_short=item__context__name_short_2,
    )
    if not result_2:
        return [{"status": 404, "step": 2}]

    result_3 = await tables.Item.objects().where(tables.Item.id == result_2[0].item)
    return [
        {
            "status": 200,
            "source_context": item__context__name_short,
            "source_word": item__text,
            "target_context": item__context__name_short_2,
            "target_word": result_3[0].text,
        }
    ]

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
