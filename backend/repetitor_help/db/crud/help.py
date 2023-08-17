from uuid import UUID

from asyncpg import ForeignKeyViolationError

from repetitor_help import tables
from repetitor_help.api.v1.help.serializers import (
    GetHelpRequest,
    UpdateHelpRequest,
    CreateHelpRequest,
)


async def create(**kwargs: CreateHelpRequest) -> UUID | str:
    """
    Create new help.
    Parameters:
        - relation: UUID of item relation, used for ForeignKey links with Item Relation, required
        - item: UUID of item, used for ForeignKey links with Item, required

    Return:
    - Help.id: UUID - primary key for new Help record - UUID type
    - str - error message in case of invalid foreign keys
    """
    # check_exists = await get(**kwargs)
    # if check_exists:  # якщо існує  такий запис
    #     return (
    #         f"an object with such parameters already exists id={check_exists[0].id}  "
    #         f"is_active={check_exists[0].is_active} "
    #     )
    #     raise TypeError(
    #         f"an object with such parameters already exists {check_exists[0].id}"
    #     )

    try:
        # result = await tables.Help.insert(tables.Help(**kwargs)).returning(
        #     tables.Help.id
        # )
        #  чат переробив  функцію на get_or_create
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

    if result._was_created:  # якщо запис щойно був створений
        return result["id"]
    else:  # якщо запис вже існував
        return (
            f"an object with such parameters already exists id={result.id}  "
            f"is_active={result.is_active} "
        )
    # return result["id"]


async def get(**get_param: GetHelpRequest) -> list[tables.Help]:
    """
    Get a list of existing help according to match conditions:
        Parameters:
        - id: UUID of Help
        - relation: UUID of item relation, used for foreign key links with item Relation
        - item: UUID of item, used for foreign key links with Item
        - is_active: bool
        - advanced options for filtering:
            - item__author: author of item, used for foreign key links with Item
            - ontext__name_short: the name of the required items context, used for foreign key links with Item - str
            - item__text: the text of the required items, used for foreign key links with Item - str type len(2..255)

    Return:
    - List that contains the results of the query, serialized to the Help type
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

    result = await query
    return result if result else []


async def update(id: UUID, **update_param: UpdateHelpRequest) -> UUID | None:
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
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update help must be UUID-type, but got {type(id)}"
        )
    filtered_param = {k: v for k, v in update_param.items() if v is not None}
    result = (
        await tables.Help.update(filtered_param)
        .where(tables.Help.id == id)
        .returning(tables.Help.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete help with help.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_help must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
