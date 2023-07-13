import uuid
from typing import Annotated
from uuid import UUID

from fastapi import Query

from repetitor_backend import tables
from repetitor_backend.db.crud import item, question, right_answ_item, item_relation

MICROSOFT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")


async def pre_processing(user_tg_id: UUID | int) -> dict:
    query = tables.CustomerContext.objects().where(
        tables.CustomerContext.is_active == True
    )
    if isinstance(user_tg_id, UUID):
        query = query.where(tables.CustomerContext.customer == user_tg_id)
    elif isinstance(user_tg_id, int):
        query = query.where(tables.CustomerContext.customer.tlg_user_id == user_tg_id)
    else:
        raise TypeError(
            f"argument function 'pre_processing' must be int or UUID, but gotten type {type(user_tg_id)}"
        )

    query = query.order_by(tables.CustomerContext.last_date, ascending=False).first()
    result_all_fk = await query.prefetch(tables.CustomerContext.all_related())
    return dict(
        context_1_id_sn=(
            result_all_fk.context_1.id,
            result_all_fk.context_1.name_short,
        ),
        context_2_id_sn=(
            result_all_fk.context_2.id,
            result_all_fk.context_2.name_short,
        ),
        author=result_all_fk.customer.id,
    )
    pass


async def creating_phrases(
        source_text: str,
        target_text: str,
        context_1_id_sn: tuple[UUID, str],
        context_2_id_sn: tuple[UUID, str],
        author: UUID = MICROSOFT_UUID,
        explanation: UUID = "00000000-0000-0000-0000-000000000010",
        type: UUID = "00000000-0000-0000-0000-000000000020",
        is_active: bool = True,
) -> list:
    1 == 1

    create_item_relation = await item_relation.create(
        author=author, explanation=explanation, type=type
    )

    # create_item_for_question = await item.create(
    #     author=author,
    #     context=context_1_id_sn[0],
    #     text=source_text,
    # )
    create_item_for_question = await tables.Item.objects().get_or_create(
        (tables.Item.context == context_1_id_sn[0])
        & (tables.Item.text == source_text)
        & (tables.Item.author == author),
    )

    # create_item_for_right_answ_item = await item.create(
    #     author=author,
    #     context=context_2_id_sn[0],
    #     text=target_text,
    # )
    create_item_for_right_answ_item = await tables.Item.objects().get_or_create(
        (tables.Item.context == context_2_id_sn[0])
        & (tables.Item.text == target_text)
        & (tables.Item.author == author),
    )
    create_question = await question.create(
        relation=create_item_relation,
        item=create_item_for_question,
    )
    create_right_answ_item = await right_answ_item.create(
        relation=create_item_relation,
        item=create_item_for_right_answ_item,
    )

    return [
        dict(
            item_relation=create_item_relation,
            item_text_1=source_text,
            item_author_1=author,
            item_context_name_short_1=context_1_id_sn[1],
            question=create_question,
            right_answ_item=create_right_answ_item,
            item_text_2=target_text,
            item_author_2=author,
            item_context_name_short_2=context_2_id_sn[1],
            is_active=True,
        )
    ]


async def get_words_from_the_db(
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
    list_item_author.append(MICROSOFT_UUID)
    queue = tables.ItemRelationView.select()
    queue = queue.where(
        (tables.ItemRelationView.is_active == is_active)
        & tables.ItemRelationView.item_author_1.is_in(list_item_author)
        & tables.ItemRelationView.item_author_2.is_in(list_item_author)
        & (  # <- тут end порівняння
                (
                        (tables.ItemRelationView.item_text_1 == item_text)
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
    ).order_by(
        tables.ItemRelationView.item_author_1,
        tables.ItemRelationView.item_author_2,
        ascending=False,
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
