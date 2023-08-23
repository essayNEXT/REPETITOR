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


async def helps_less_max_impressions(
    list_of_helps: list[tables.Help],
) -> tables.Help:
    """
    Helps Less Max Impressions

    This method takes a list of Help objects and returns a Help object with the least total impressions,
    if the total impressions of the first Help object in the list is less than a predefined MAX_IMPRESSIONS value.
    If the total impressions of the first Help object is greater than or equal to MAX_IMPRESSIONS,
    the method sorts the list based on the ratio of positive feedback to total impressions
    and deletes all Help objects except the one with the highest ratio. The remaining Help object is then returned.

    Parameters:
    - list_of_helps (List[tables.Help]): The list of Help objects to process.

    Returns:
    - tables.Help: The Help object with the least total impressions or
    the Help object with the highest ratio of positive feedback to total impressions, after deleting other Help objects.

    """
    if list_of_helps[0].total_impressions >= MAX_IMPRESSIONS:
        results_sorted = sorted(
            list_of_helps,
            key=lambda h: (
                (h.positive_feedback - h.negative_feedback) / h.total_impressions
            ),
        )
        for element in results_sorted[:-1]:
            await delete_help(element.id)
        fin_result = results_sorted[0]
    else:
        fin_result = list_of_helps[0]
    return fin_result


@router.post("/help/")
async def create_help(
    new_help: CreateHelpRequest,
) -> UUID | str:
    """
    Creates a new help entry in the database.

    Parameters:
    - `front_name` (str): The front name of the help, required.
    - `state` (str): The state of the help, required.
    - `text` (str): The text of the help, required.
    - `language` (UUID): The language of the help, required.

    - `auto_translation` (bool|None): Flag for auto translation.
    - `positive_feedback` (int|None): The positive feedback count of the help.
    - `negative_feedback` (int|None): The negative feedback count of the help.
    - `total_impressions` (int|None): The total impressions count of the help.

    Returns:
    - UUID: The ID of the created help entry.
    - str - error message in case of invalid foreign keys.

    """
    result = await help.create(**new_help.dict())
    return result["id"]


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
    positive_feedback: int | None = None,
    negative_feedback: int | None = None,
    total_impressions: int | None = None,
    language__name_short: Annotated[str, Query(min_length=2, max_length=10)] = None,
) -> list:
    """

    This method `get_help` retrieves help information based on the provided parameters.

    Parameters:
    - `front_name` (str, Query): The front name of the help.
    - `customer_tg_id` (UUID|int): The customer's Telegram ID or UUID.
    - `state` (str, Query): The state of the help.
    - `auto_translation` (bool|None): Flag for auto translation.
    - `id` (UUID|None): The ID of the help.
    - `text` (str|None, Query): The text of the help.
    - `language` (UUID): The language of the help.
    - `is_active` (bool): Flag indicating if the help is active.
    - `modified_on` (pydantic_datetime): The modified timestamp of the help.
    - `positive_feedback` (int|None): The positive feedback count of the help.
    - `negative_feedback` (int|None): The negative feedback count of the help.
    - `total_impressions` (int|None): The total impressions count of the help.
    - `language__name_short` (str, Query): The short name of the language.

    Returns:
    - list[tables.Help]: The list of help responses based on the provided parameters.

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
            # Якщо перекладу не дали.
            raise ValueError(
                "У рамках поточного контексту не можемо знайти переклад.Пропонуємо надати свій варіант, якщо він є"
            )

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
        results = await help.create(**new_help.dict())
        results = [results]
    # тепер якщо переклад хелпа здайдено в БД
    elif len(helps) == 1:
        results = helps

    else:  # хз, тут  helps_less_max_impressions
        helps_sorted = sorted(helps, key=lambda h: h.total_impressions)
        helps_after_preprocess = await helps_less_max_impressions(helps_sorted)
        results = [helps_after_preprocess]

    # фінальна обробка результату
    fin_result = [
        result.to_dict() for result in results if isinstance(result, tables.Help)
    ]
    return fin_result


@router.patch("/help/")
async def update_help(id: UUID, update_param_help: UpdateHelpRequest) -> UUID | None:
    """
    Updates the help entry with the specified ID.

    Parameters:
    - `id` (UUID): The ID of the help, required
    - `front_name` (str): The front name of the help.
    - `customer_tg_id` (UUID|int): The customer's Telegram ID or UUID.
    - `state` (str): The state of the help.
    - `auto_translation` (bool|None): Flag for auto translation.
    - `text` (str|None): The text of the help.
    - `language` (UUID): The language of the help.
    - `is_active` (bool): Flag indicating if the help is active.
    - `modified_on` (pydantic_datetime): The modified timestamp of the help.
    - `positive_feedback` (int|None): The positive feedback count of the help.
    - `negative_feedback` (int|None): The negative feedback count of the help.
    - `total_impressions` (int|None): The total impressions count of the help.
    - `language__name_short` (str): The short name of the language.
    -  advanced options:
        - `modifying_positive_feedback` (int|None): You can add / subtract values to the positive feedback count.
        - `modifying_negative_feedback` (int|None): You can add / subtract values to the negative feedback count.
        - `modifying_total_impressions` (int|None): You can add / subtract values to the total impressions count.

    Result:
    - UUID | None: The updated help entry ID, or None if the update was unsuccessful.

    """
    return await help.update(id=id, **update_param_help.dict())


@router.delete("/help/")
async def delete_help(id_param: UUID) -> UUID | None:
    """
    Delete help with help.id == id.

    Parameter:
    - `id` (UUID): The ID of the help, required

    Result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """

    return await help.delete(id_param)
