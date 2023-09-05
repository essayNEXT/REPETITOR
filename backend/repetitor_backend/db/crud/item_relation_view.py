import uuid
from uuid import UUID

from repetitor_backend import tables
from repetitor_backend.db.crud import question, right_answ_item, item_relation

MICROSOFT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")
GOOGLE_UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")

REPETITOR_EXPLANATION_UUID = uuid.UUID("00000000-0000-0000-0000-000000000010")
REPETITOR_TYPE_UUID = uuid.UUID("00000000-0000-0000-0000-000000000020")

TRUSTED_USER_CUSTOMER_TYPE = "translator"


async def creating_phrases(
    source_text: str,
    target_text: str,
    context_1_id_sn: tuple[UUID, str],
    context_2_id_sn: tuple[UUID, str],
    author: UUID = MICROSOFT_UUID,
    explanation: UUID = REPETITOR_EXPLANATION_UUID,
    type: UUID = REPETITOR_TYPE_UUID,
    is_active: bool = True,
) -> list:
    """
    Додає в БД два слова(source_text та target_text), у контексті(context_1_id_sn, context_2_id_sn)
    для  автор (author), які мають сформований переклад
    на основі зв'язку через таблиці Question|RightAnswItem і додаткову М2М таблицю ItemRelation.

    Parameters:
    - source_text: str type, max lenght is 255 symbols - source word, required
    - target_text: str type, max lenght is 255 symbols - target word, required
    - context_1_id_sn: tuple[UUID, str] - UUID and the short name of the required items context, required
    - context_2_id_sn: tuple[UUID, str] - UUID and the short name of the required items context, required
    - author: UUID - UUID, corresponds to the parameter tables.Customer.id
    - explanation: UUID, corresponds to the parameter tables.Explanation.id
    - type: UUID, corresponds to the parameter tables.RelationType.id
    - is_active: bool = True

    Return:
    - Список, що містить результати запиту. Структура результату відповідає наступній структурі:
        - item_relation: UUID of item relation,
        - item_text_1: str type - перше слово з пари у представлені, необов'язково що це source слово ,
        - item_author_1: UUID - автор слова №1, який створив об'єкт у БД,
        - context_1_id_sn: tuple[UUID, str] - UUID та коротке ім'я слова №1,
        - item_text_2: str type - друге слово з пари у представлені, це target слово,
        - item_author_2: UUID - автор слова №2, який створив об'єкт у БД,
        - context_1_id_sn: tuple[UUID, str] - UUID та коротке ім'я слова №2,
        - question: UUID - запис через який відбуваються зв'язки слів у контекстні пари,
        - right_answ_item: UUID - запис через який відбуваються зв'язки слів у контекстні пари,
        - is_active: bool
    """

    create_item_relation = await item_relation.create(
        author=author, explanation=explanation, type=type
    )

    create_item_for_question = await tables.Item.objects().get_or_create(
        (tables.Item.context == context_1_id_sn[0])
        & (tables.Item.text == source_text)
        & (tables.Item.author == author),
    )

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
            context_1_id_sn=context_1_id_sn,
            question=create_question,
            right_answ_item=create_right_answ_item,
            item_text_2=target_text,
            item_author_2=author,
            context_2_id_sn=context_2_id_sn,
            is_active=is_active,
        )
    ]


async def get_words_from_the_db(
    item_text: str,
    list_item_author: list[UUID],
    context_1_id_sn: tuple[UUID, str],
    context_2_id_sn: tuple[UUID, str],
    is_active: bool = True,
) -> list[tables.ItemRelationView]:
    """
    Отримати список можливих перекладів у контексті(item_context_name_short_1, item_context_name_short_2)
    для слова(item_text) авторів (item_author), які мають сформований переклад
    на основі зв'язку через таблиці Question|RightAnswItem і додаткову М2М таблицю ItemRelation.

    Parameters:
    - item_text: str type, max lenght is 255 symbols - target word, required
    - item_author: UUID of customer, used for ForeignKey links with Customer, required
    - context_1_id_sn: tuple[UUID, str] - UUID and the short name of the required items context, required
    - context_2_id_sn: tuple[UUID, str] - UUID and the short name of the required items context, required
    - is_active: bool = True

    Return:
    - Список, що містить результати запиту. Структура результату відповідає структурі згенерованого представлення.
    Схема записів у представлені наступна:
        - item_relation: UUID of item relation,
        - item_text_1: str type - перше слово з пари у представлені, це source слово,
        - item_author_1: UUID - автор слова №1, який створив об'єкт у БД,
        - context_1_id_sn: tuple[UUID, str] - UUID та коротке ім'я слова №1,
        - item_text_2: str type - друге слово з пари у представлені, це target слово,
        - item_author_2: UUID - автор слова №2, який створив об'єкт у БД,
        - context_1_id_sn: tuple[UUID, str] - UUID та коротке ім'я слова №2,
        - question: UUID - запис через який відбуваються зв'язки слів у контекстні пари,
        - right_answ_item: UUID - запис через який відбуваються зв'язки слів у контекстні пари,
        - is_active: bool
    """
    # list_item_author.append(MICROSOFT_UUID)
    query = tables.ItemRelationView.select()
    query = query.where(
        (tables.ItemRelationView.is_active == is_active)
        & (
            (
                tables.ItemRelationView.item_author_1.customer_type.name
                == TRUSTED_USER_CUSTOMER_TYPE
            )
            | tables.ItemRelationView.item_author_1.is_in(list_item_author)
        )
        & (
            (
                tables.ItemRelationView.item_author_2.customer_type.name
                == TRUSTED_USER_CUSTOMER_TYPE
            )
            | tables.ItemRelationView.item_author_2.is_in(list_item_author)
        )
        & (  # <- тут and порівняння
            (
                (tables.ItemRelationView.item_text_1 == item_text)
                & (
                    tables.ItemRelationView.item_context_name_short_1.is_in(
                        [context_1_id_sn[1], context_2_id_sn[1]]
                    )
                    & tables.ItemRelationView.item_context_name_short_2.is_in(
                        [context_1_id_sn[1], context_2_id_sn[1]]
                    )
                )
            )
            | (  # <- тут or порівняння
                (tables.ItemRelationView.item_text_2 == item_text)
                & (
                    tables.ItemRelationView.item_context_name_short_1.is_in(
                        [context_1_id_sn[1], context_2_id_sn[1]]
                    )
                    & tables.ItemRelationView.item_context_name_short_2.is_in(
                        [context_1_id_sn[1], context_2_id_sn[1]]
                    )
                )
            )
        )
    ).order_by(  # сортування за авторством, оскільки МС та гугл моють №0000 та № 0001, то їх переклади будуть y кінці
        tables.ItemRelationView.item_author_1,
        tables.ItemRelationView.item_author_2,
        ascending=False,
    )
    result = await query
    # міняю місцями щоб спочатку було source блок(i1, a1, c1), а потім target блок(i2, a2, c2)
    for i in result:
        if i["item_text_2"] == item_text:
            i["item_text_1"], i["item_text_2"] = i["item_text_2"], i["item_text_1"]
            i["item_author_1"], i["item_author_2"] = (
                i["item_author_2"],
                i["item_author_1"],
            )
            i["item_context_name_short_1"], i["item_context_name_short_2"] = (
                i["item_context_name_short_2"],
                i["item_context_name_short_1"],
            )
        # йде заміна результату даних контексту.
        # - замість item_context_name_short_1(де тільки коротка назва uk),
        # + вноситься context_1_id_sn tuple[UUID, str] - UUID та коротке ім'я
        i["context_1_id_sn"] = (
            context_1_id_sn
            if i.pop("item_context_name_short_1") == context_1_id_sn[1]
            else context_2_id_sn
        )
        i["context_2_id_sn"] = (
            context_2_id_sn
            if i.pop("item_context_name_short_2") == context_2_id_sn[1]
            else context_1_id_sn
        )

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
