import uuid
from uuid import UUID
from fastapi import APIRouter

from repetitor_backend.db.crud.item_relation_view import (
    MICROSOFT_UUID,
    REPETITOR_EXPLANATION_UUID,
    REPETITOR_TYPE_UUID,
)
from repetitor_backend.external_api.microsoft import translate
from .serializers import (
    GetItemRelationViewResponse,
    CreatingPhrasesRequest,
)
from repetitor_backend.db.crud import item_relation_view, customer_context
import logging

logger = logging.getLogger()

router = APIRouter()


@router.post(
    "/creating_phrases/",
    response_model=list[GetItemRelationViewResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def creating_phrases(new_creating_phrases: CreatingPhrasesRequest) -> list:
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
    result = await item_relation_view.creating_phrases(
        source_text=new_creating_phrases.source_text.strip().lower(),
        target_text=new_creating_phrases.target_text.strip().lower(),
        context_1_id_sn=new_creating_phrases.context_1_id_sn,
        context_2_id_sn=new_creating_phrases.context_2_id_sn,
        author=new_creating_phrases.author or MICROSOFT_UUID,
        explanation=new_creating_phrases.explanation or REPETITOR_EXPLANATION_UUID,
        type=new_creating_phrases.type or REPETITOR_TYPE_UUID,
        is_active=new_creating_phrases.is_active,
    )

    return result


@router.get(
    "/translate/",
    response_model=list[GetItemRelationViewResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_translate(
    item_text: str,
    customer_tg_id: UUID | int,
    is_active: bool = True,
) -> list:
    """
    Уже 2версія, пошук слів у БД, якщо не знайшло, то перекладає через мікрософт, а потім отриману пару слів додає в БД.
    Отримати список можливих перекладів у контексті(context_1_id_sn, context_2_id_sn)
    для слова(item_text) авторів (item_author), які мають сформований переклад
    на основі зв'язку через таблиці Question|RightAnswItem і додаткову М2М таблицю ItemRelation.

    Parameters:
    - item_text: str type, max lenght is 255 symbols - source word, required
    - customer_tg_id: UUID|int, required
        - if customer_tg_id == UUID, corresponds to the parameter tables.Customer.id
        - if customer_tg_id == int, corresponds to the parameter tables.Customer.tlg_user_id
    - is_active: bool = True

    Return:
    - Список, що містить результати запиту. Структура результату відповідає структурі згенерованого представлення.
    Схема записів у представлені наступна:
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

    item_text = item_text.strip().lower()

    result_pre_processing: dict = (
        await customer_context.get_the_latest_context_based_on_customer_tg_id(
            customer_tg_id
        )
    )
    context_1_id_sn = result_pre_processing.get("context_1_id_sn", None)
    context_2_id_sn = result_pre_processing.get("context_2_id_sn", None)
    item_author = result_pre_processing.get("author", None)

    # заглушка, для додавання до авторів гугла та мікрософт у майбутньому
    list_item_author = [item_author]

    result_get_words_from_the_db = await item_relation_view.get_words_from_the_db(
        item_text=item_text,
        list_item_author=list_item_author,
        context_1_id_sn=context_1_id_sn,
        context_2_id_sn=context_2_id_sn,
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
        # Якщо перекладу не дали. ТУТ треба доробляти, Бо програма буде падати, якщо True
        target_tex = "У рамках поточного контексту не можемо знайти переклад.Пропонуємо надати свій варіант, якщо він є"

        return [
            dict(
                item_relation=uuid.uuid4(),  # фейкові, рандомні id
                item_text_1=source_text,
                item_author_1=item_author,
                context_1_id_sn=context_1_id_sn,
                question=uuid.uuid4(),  # фейкові, рандомні id
                right_answ_item=uuid.uuid4(),  # фейкові, рандомні id
                item_text_2=target_tex,
                item_author_2=item_author,
                context_2_id_sn=context_2_id_sn,
                is_active=is_active,
            )
        ]

        # привожу до 1 правила, source=context1, target=cntxt2
    if result_translate[1] == context_1_id_sn[1]:
        context_1_id_sn, context_2_id_sn = context_2_id_sn, context_1_id_sn
    target_text = result_translate[0]

    #
    # створення нової пари слів у БД на основі
    result_creating_phrases = await item_relation_view.creating_phrases(
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
