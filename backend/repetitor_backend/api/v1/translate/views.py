from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from .serializers import (
    GetItemRelationViewResponse,
)
from repetitor_backend.db.crud import (
    item_relation_view,
)
import logging
from repetitor_backend.external_api.microsoft import translate

logger = logging.getLogger()

router = APIRouter()


@router.get(
    "/translate/",
    response_model=list[GetItemRelationViewResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_translate(
    item_text: str,
    item_author: UUID,
    item_context_name_short_1: Annotated[str, Query(min_length=2, max_length=10)],
    item_context_name_short_2: Annotated[str, Query(min_length=2, max_length=10)],
    is_active: bool = True,
) -> list:
    """
    Поки тільки 1 версія, пошук тільки слів у БД.
    Отримати список можливих перекладів у контексті(item_context_name_short_1, item_context_name_short_2)
    для слова(item_text) авторів (item_author), які мають сформований переклад
    на основі зв'язку через таблиці Question|RightAnswItem і додаткову М2М таблицю ItemRelation.

    Parameters:
    - item_text: str type, max lenght is 255 symbols - target word
    - item_author: UUID of customer, used for ForeignKey links with Customer
    - item_context_name_short_1: str type - the short name of the required items context
    - item_context_name_short_2: str type - the short name of the required items context
    - is_active: bool = True

    Return:
    - Список, що містить результати запиту. Структура результату відповідає структурі згенерованого представлення.
    Схема записів у представлені наступна:
        - item_relation: UUID of item relation,
        - item_text_1: str type - перше слово з пари у представлені, необов'язково що це source слово ,
        - item_author_1: UUID - автор слова №1, який створив об'єкт у БД,
        - item_context_name_short_1: str type - мова слова №1,
        - item_text_2: str type - друге слово з пари у представлені, необов'язково що це target слово ,
        - item_author_2: UUID - автор слова №2, який створив об'єкт у БД,
        - item_context_name_short_2: str type - мова слова №2,
        - question: UUID - запис через який відбуваються зв'язки слів у контекстні пари,
        - right_answ_item: UUID - запис через який відбуваються зв'язки слів у контекстні пари,
        - is_active: bool
    """
    # заглушка, для додавання до авторів гугла та мікрософт у майбутньому
    list_item_author = [item_author]
    result = await item_relation_view.get(
        item_text=item_text,
        list_item_author=list_item_author,
        item_context_name_short_1=item_context_name_short_1,
        item_context_name_short_2=item_context_name_short_2,
        is_active=is_active,
    )

    return result


@router.delete("/translate/")
async def delete_translate(id: UUID) -> UUID | None:
    """
    Delete item relation with ItemRelation.id == id.

    Parameter:
    - id - UUID.

    Result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await translate.delete(id)
