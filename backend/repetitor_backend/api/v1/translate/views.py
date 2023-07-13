from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Query

from repetitor_backend.db.crud.item_relation_view import (
    pre_processing,
    creating_phrases,
)
from repetitor_backend.external_api.microsoft import translate
from .serializers import (
    GetItemRelationViewResponse,
)
from repetitor_backend.db.crud import (
    item_relation_view,
    item_relation,
    item,
    question,
    right_answ_item,
)
import logging

logger = logging.getLogger()

router = APIRouter()


# @router.get(
#     "/creating_phrases/",
#     # response_model=List[ItemRelationViewResponse],
#     # response_model_exclude_none=True,
#     # response_model_exclude={"is_active"},
# )


######################


@router.get(
    "/translate/",
    response_model=list[GetItemRelationViewResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_translate(
    item_text: str,
    user_tg_id: UUID | int,
    item_context_name_short_1: Annotated[str, Query(min_length=2, max_length=10)]
    | None = None,
    item_context_name_short_2: Annotated[str, Query(min_length=2, max_length=10)]
    | None = None,
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

    result_pre_processing: dict = await pre_processing(user_tg_id)
    context_1_id_sn = result_pre_processing.get("context_1_id_sn", None)
    context_2_id_sn = result_pre_processing.get("context_2_id_sn", None)
    item_author = result_pre_processing.get("author", None)

    # заглушка, для додавання до авторів гугла та мікрософт у майбутньому
    list_item_author = [item_author]

    result_get_words_from_the_db = await item_relation_view.get_words_from_the_db(
        item_text=item_text,
        list_item_author=list_item_author,
        item_context_name_short_1=context_1_id_sn[1],
        item_context_name_short_2=context_2_id_sn[1],
        is_active=is_active,
    )

    if result_get_words_from_the_db:
        print("result_get_words_from_the_db")
        return result_get_words_from_the_db
    #
    # шукаємо переклади пари слів
    source_text = item_text
    result_translate = await translate(
        source_lng=context_1_id_sn[1], target_lng=context_2_id_sn[1], text=source_text
    )

    if len(result_translate) < 2:
        return (
            f"пишемо що для данного варіанта в рамках поточного контексту не можемо знайти переклад "
            f"і пропонуємо надати свій варіант, якщо він є"
        )

        # привожу до 1 правила, source=context1, target=cntxt2
    if result_translate[1] == context_1_id_sn[1]:
        context_1_id_sn, context_2_id_sn = context_2_id_sn, context_1_id_sn
    target_text = result_translate[0]

    #
    # створення нової пари слів у БД на основі
    result_creating_phrases = await creating_phrases(
        source_text=source_text,
        target_text=target_text,
        context_1_id_sn=context_1_id_sn,
        context_2_id_sn=context_2_id_sn,
    )

    return result_creating_phrases


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

    return await item_relation_view.delete(id)
