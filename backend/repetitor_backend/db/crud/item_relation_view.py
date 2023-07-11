from typing import Annotated
from uuid import UUID

from fastapi import Query

from repetitor_backend import tables


async def get(
    item_text: str,
    list_item_author: list[UUID],
    item_context_name_short_1: Annotated[str, Query(min_length=2, max_length=10)],
    item_context_name_short_2: Annotated[str, Query(min_length=2, max_length=10)],
    is_active: bool = True,
) -> list[tables.ItemRelationView]:
    """
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

    queue = tables.ItemRelationView.select()
    queue = queue.where(
        (tables.ItemRelationView.is_active == is_active)
        & (  # <- тут end порівняння
            (
                (tables.ItemRelationView.item_text_1 == item_text)
                & tables.ItemRelationView.item_author_1.is_in(list_item_author)
                & (
                    tables.ItemRelationView.item_context_name_short_1.is_in(
                        [item_context_name_short_1, item_context_name_short_2]
                    )
                    & tables.ItemRelationView.item_context_name_short_2.is_in(
                        [item_context_name_short_1, item_context_name_short_2]
                    )
                )
            )
            | (  # <- тут or порівняння
                (tables.ItemRelationView.item_text_2 == item_text)
                & tables.ItemRelationView.item_author_2.is_in(list_item_author)
                & (
                    tables.ItemRelationView.item_context_name_short_1.is_in(
                        [item_context_name_short_1, item_context_name_short_2]
                    )
                    & tables.ItemRelationView.item_context_name_short_2.is_in(
                        [item_context_name_short_1, item_context_name_short_2]
                    )
                )
            )
        )
    )
    result = await queue

    return result


async def delete(id: UUID) -> UUID | None:
    """Delete item relation with item_relation_view.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_item_relation_view must be UUID-type, but got {type(id)}"
        )
    result = (
        await tables.ItemRelation.update(is_active=False)
        .where(tables.ItemRelation.id == id)
        .returning(tables.ItemRelation.id)
    )
    return result[0]["id"] if result else None
