import logging
from uuid import UUID

from asyncpg import ForeignKeyViolationError
from fastapi import HTTPException, status

from repetitor_help import tables
from repetitor_help.api.v1.help.serializers import (
    GetHelpRequest,
    UpdateHelpRequest,
    CreateHelpRequest,
)

logger = logging.getLogger()


async def create(**kwargs: CreateHelpRequest) -> tables.Help | str:
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
    -
    - tables.Help: a database object that corresponds to the description of the tables.Help.
    - str - error message in case of invalid foreign keys.

    """

    try:
        query_conditions = [
            getattr(tables.Help, key) == value
            for key, value in kwargs.items()
            if value is not None
        ]
        query_final = query_conditions[0]
        for query in query_conditions[1:]:
            query_final &= query

        result = await tables.Help.objects().get_or_create(query_final)

    except ForeignKeyViolationError as e:
        return str(e)  # якщо  невірні зовнішні ключі передані

    return result


async def get(**get_param: GetHelpRequest) -> list[tables.Help]:
    """

    This method `get_help` retrieves help information based on the provided parameters.

    Parameters:
    - `front_name` (str|None): The front name of the help.
    - `customer_tg_id` (UUID|int): The customer's Telegram ID or UUID.
    - `state` (str|None): The state of the help.
    - `auto_translation` (bool|None): Flag for auto translation.
    - `id` (UUID|None): The ID of the help.
    - `text` (str|None): The text of the help.
    - `language` (UUID|None): The language of the help.
    - `is_active` (bool|None): Flag indicating if the help is active.
    - `modified_on` (pydantic_datetime): The modified timestamp of the help.
    - `positive_feedback` (int|None): The positive feedback count of the help.
    - `negative_feedback` (int|None): The negative feedback count of the help.
    - `total_impressions` (int|None): The total impressions count of the help.
    - `language__name_short` (str|None): The short name of the language.

    Returns:
    - list[tables.Help]: The list of help responses based on the provided parameters.

    """

    query = tables.Help.objects()

    for param, value in get_param.items():
        if value is not None:
            nested_attr = tables.Help
            # Розбиваємо параметр на частини
            parts = param.split("__")

            for part in parts:
                nested_attr = getattr(nested_attr, part, None)

            query = query.where(nested_attr == value)

    result = await query.prefetch(tables.Help.all_related())
    return result if result else []


async def update(id: UUID, **update_param: UpdateHelpRequest) -> UUID | None:
    """
    Updates the help entry with the specified ID.

    Parameters:
    - `id` (UUID): The ID of the help, required
    - `front_name` (str|None): The front name of the help.
    - `state` (str|None): The state of the help.
    - `auto_translation` (bool|None): Flag for auto translation.
    - `text` (str|None): The text of the help.
    - `language` (UUID|None): The language of the help.
    - `is_active` (bool|None): Flag indicating if the help is active.
    - `modified_on` (pydantic_datetime|None): The modified timestamp of the help.
    - `positive_feedback` (int|None): The positive feedback count of the help.
    - `negative_feedback` (int|None): The negative feedback count of the help.
    - `total_impressions` (int|None): The total impressions count of the help.
    -  advanced options:
        - `modifying_positive_feedback` (int|None): You can add / subtract values to the positive feedback count.
        - `modifying_negative_feedback` (int|None): You can add / subtract values to the negative feedback count.
        - `modifying_total_impressions` (int|None): You can add / subtract values to the total impressions count.

    Result:
    - UUID | None: The updated help entry ID, or None if the update was unsuccessful.

    """
    if not isinstance(id, UUID):
        logging.error(
            f"parameter 'id' for function update help must be UUID-type, but got {type(id)}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"parameter 'id' for function update help must be UUID-type, but got {type(id)}",
        )

    filtered_param = {k: v for k, v in update_param.items() if v is not None}
    # https://piccolo-orm.readthedocs.io/en/latest/piccolo/query_types/update.html#integer-columns
    # # Add 100 to the total_impressions of each help:
    # await Help.update({ Help.total_impressions: Help.total_impressions + 100 },)
    keys_to_be_deleted = [
        k for k, v in filtered_param.items() if k.startswith("modifying_")
    ]  # шукаємо усі 'modifying_'ключі, щоб потім по них пройтися
    for key in keys_to_be_deleted:
        new_k = key.replace("modifying_", "")  # створюємо новий ключ без modifying_
        filtered_param[new_k] = getattr(tables.Help, new_k, None) + filtered_param[key]
        del filtered_param[key]  # видаляємо стару пару ключ-значення

    result = (
        await tables.Help.update(filtered_param)
        .where(tables.Help.id == id)
        .returning(tables.Help.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """
    Delete help with help.id == id.

    Parameter:
    - `id` (UUID): The ID of the help, required

    Result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        logging.error(
            f"parameter 'id' for function del_help must be UUID-type, but got {type(id)}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"parameter 'id' for function del_help must be UUID-type, but got {type(id)}",
        )
    result = await update(id=id, is_active=False)
    return result
