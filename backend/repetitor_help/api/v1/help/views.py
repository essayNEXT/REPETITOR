import logging

from typing import List, Annotated
from uuid import UUID
from fastapi import APIRouter, Query
from pydantic.validators import datetime as pydantic_datetime

from repetitor_backend.api.v1.context.views import get_context
from repetitor_backend.external_api.translate import translate
from repetitor_backend.db.crud.customer import get_customer
from repetitor_help import tables
from .serializers import (
    CreateHelpRequest,
    UpdateHelpRequest,
    GetHelpRequest,
    GetHelpResponse,
)
from repetitor_help.db.crud import help

MAX_IMPRESSIONS = 100

logger = logging.getLogger()

router = APIRouter()


def helps_less_max_impressions(list_of_helps: list[tables.Help]) -> list[tables.Help]:
    return [list_of_helps[0]]


@router.post("/help/")
async def create_help(
    new_help: CreateHelpRequest,
) -> UUID | str:
    """
    Create new help.
    Parameters:
    - relation: UUID of item relation, used for ForeignKey links with Item Relation, required
    - item: UUID of item, used for ForeignKey links with Item, required

    Return:
    - Help.id: UUID - primary key for new help record - UUID type
    - str - error message in case of invalid foreign keys
    """
    return await help.create(**new_help.dict())


# стандартний гет
@router.get(
    "/help1/",
    response_model=List[GetHelpResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_help1(
    id: UUID | None = None,
    text: Annotated[str | None, Query(min_length=2, max_length=255)] = None,
    language: UUID = None,
    state: Annotated[str | None, Query(min_length=2, max_length=255)] = None,
    is_active: bool = True,
    auto_translation: bool | None = True,
    modified_on: pydantic_datetime = None,
    positive_feedback: int | None = 0,
    negative_feedback: int | None = 0,
    total_impressions: int | None = 0,
    language__name_short: Annotated[str, Query(min_length=2, max_length=10)] = None,
) -> list:
    """
    Get a list of existing help according to match conditions:
    Parameters:
    - id: UUID of Help
    - relation: UUID of item relation, used for ForeignKey links with Item Relation
    - item: UUID of item, used for ForeignKey links with Item
    - is_active: bool
    - advanced options for filtering:
        - item__author: author of item, used for ForeignKey links with Item
        - item__context__name_short: the short name of the required items context, used for FK links with Item - str
        - item__text: the text of the required items, used for ForeignKey links with Item - str type len(2..255)

    Return:
    - List that contains the results of the query, serialized to
    the Help type
    """
    get_param_help = GetHelpRequest(
        id=id,
        text=text,
        language=language,
        state=state,
        is_active=is_active,
        auto_translation=auto_translation,
        modified_on=modified_on,
        total_impressions=total_impressions,
        positive_feedback=positive_feedback,
        negative_feedback=negative_feedback,
        language__name_short=language__name_short,
    )
    results = await help.get(**get_param_help.dict())
    fin_result = [
        result.to_dict() for result in results if isinstance(result, tables.Help)
    ]
    return fin_result


# гет згідно особливоо алгоритму
@router.get(
    "/help/",
    response_model=List[GetHelpResponse],
    response_model_exclude_none=True,
    response_model_exclude={"is_active"},
)
async def get_help(
    front_name: Annotated[str, Query(min_length=2, max_length=255)],
    customer_tg_id: UUID | int,
    state: Annotated[str, Query(min_length=2, max_length=255)],
    auto_translation: bool | None = None,
    id: UUID | None = None,
    text: Annotated[str | None, Query(min_length=2, max_length=255)] = None,
    language: UUID = None,
    is_active: bool = True,
    modified_on: pydantic_datetime = None,
    positive_feedback: int | None = 0,
    negative_feedback: int | None = 0,
    total_impressions: int | None = 0,
    language__name_short: Annotated[str, Query(min_length=2, max_length=10)] = None,
) -> list:
    """
    Get a list of existing help according to match conditions:
    Parameters:
    - id: UUID of Help
    - relation: UUID of item relation, used for ForeignKey links with Item Relation
    - item: UUID of item, used for ForeignKey links with Item
    - is_active: bool
    - advanced options for filtering:
        - item__author: author of item, used for ForeignKey links with Item
        - item__context__name_short: the short name of the required items context, used for FK links with Item - str
        - item__text: the text of the required items, used for ForeignKey links with Item - str type len(2..255)

    Return:
    - List that contains the results of the query, serialized to
    the Help type
    """
    customer_info = await get_customer(customer_id=customer_tg_id)
    language__name_short = (
        customer_info[0].native_language or customer_info[0].tlg_language or "en"
    )

    get_param_help = GetHelpRequest(
        id=id,
        text=text,
        language=language,
        front_name=front_name,
        state=state,
        is_active=is_active,
        auto_translation=auto_translation,
        modified_on=modified_on,
        total_impressions=total_impressions,
        positive_feedback=positive_feedback,
        negative_feedback=negative_feedback,
        language__name_short=language__name_short,
    )
    helps = await help.get(**get_param_help.dict())

    if not helps:
        get_param_help.language__name_short = "en"

        base_help = await help.get(**get_param_help.dict())
        if not base_help:
            raise ValueError(
                f"there is no help for such parameters {get_param_help.dict()}"
            )
        base_help_text = base_help[0].text
        result_translate = await translate(
            source_lng="en", target_lng=language__name_short, text=base_help_text
        )

        if len(result_translate) < 2:
            # Якщо перекладу не дали. ТУТ треба доробляти, Бо програма буде падати, якщо True
            raise ValueError(
                "У рамках поточного контексту не можемо знайти переклад.Пропонуємо надати свій варіант, якщо він є"
            )

        # class Manager(Table):
        #     name = Varchar(unique=True)
        #     email = Varchar()
        #
        # class Band(Table):
        #     name = Varchar()
        #     manager_name = Varchar()
        #
        # >>> await Band.select(
        #     ...     Band.name,
        # ...     Band.manager_name.join_on(Manager.name).email
        # ... )

        # створення перекладеного запису в БД
        language_query = await get_context(name_short=language__name_short)
        language = language_query[0]["id"]
        text = result_translate[0]
        new_help = CreateHelpRequest(
            text=text,
            language=language,
            front_name=front_name,
            state=state,
            is_active=True,
            auto_translation=True,
        )
        new_help_id = await help.create(**new_help.dict())
        results = await help.get(**GetHelpRequest(id=new_help_id).dict())
        # fin_result = [result.to_dict() for result in results if isinstance(result, tables.Help)]
        # return fin_result
        [
            dict(
                id=new_help_id,
                text=text,
                language=language,
                front_name=front_name,
                state=state,
                is_active=True,
                auto_translation=True,
                total_impressions=0,
                positive_feedback=0,
                negative_feedback=0,
                language__name_short=language__name_short,
            )
        ]

    # тепер якщо переклад хелпа здайдено в БД
    elif len(helps) == 1:
        results = helps

    else:  # хз, тут треба доробляти з незрозумілим helps_less_max_impressions
        results_sorted = sorted(helps, key=lambda r: r.modified_on, reverse=True)
        results_after_process = helps_less_max_impressions(results_sorted)
        results = results_after_process

    fin_result = [
        result.to_dict() for result in results if isinstance(result, tables.Help)
    ]
    return fin_result


@router.patch("/help/")
async def update_help(id: UUID, update_param_help: UpdateHelpRequest) -> UUID | None:
    """
    Update existing record in help.

    parameters:
    - id: UUID of Help, required
    - relation: UUID of item relation, used for ForeignKey links with Item Relation
    - item: UUID of item, used for ForeignKey links with Item
    - is_active: bool

    Return:
    - Help.id: UUID - primary key for help record - UUID type
    - If there is no record with this id, it returns None
    """

    return await help.update(id=id, **update_param_help.dict())


@router.delete("/help/")
async def delete_help(id_param: UUID) -> UUID | None:
    """
    Delete help with help.id == id.

    Parameter:
    - id - UUID.

    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await help.delete(id_param)
