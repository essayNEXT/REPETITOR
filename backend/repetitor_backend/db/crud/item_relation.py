from datetime import datetime
from uuid import UUID

from asyncpg import ForeignKeyViolationError

from repetitor_backend import tables
from repetitor_backend.api.v1.item_relation.serializers import (
    GetItemRelationRequest,
    UpdateItemRelationRequest,
    ItemRelationCreateRequest,
)


async def create(**kwargs: ItemRelationCreateRequest) -> UUID | str:
    """Create new item relation.
    Parameters:
        -

    Return:
    - ItemRelation.id: UUID - primary key for new item relation record - UUID type
    - str - error message in case of invalid foreign keys
    """
    check_exists = await get(**kwargs)
    if check_exists:  # якщо існує  такий запис
        return check_exists[0]["id"]
        return (
            f"an object with such parameters already exists id={check_exists[0].id}  "
            f"is_active={check_exists[0].is_active} "
        )
        raise TypeError(
            f"an object with such parameters already exists {check_exists[0].id}"
        )

    try:
        result = await tables.ItemRelation.insert(
            tables.ItemRelation(**kwargs)
        ).returning(tables.ItemRelation.id)
    except ForeignKeyViolationError as e:
        return str(e)
    return result[0]["id"]


async def get(**get_param: GetItemRelationRequest) -> list[tables.ItemRelation]:
    """Get a list of existing item relation according to match conditions:
        Parameters:
        - id: UUID of item relation
        - customer: UUID of customer, used for ForeignKey links with Customer
        - context_1: UUID of context, used for ForeignKey links with Context
        - context_2: UUID of context, used for ForeignKey links with Context
        - last_date: item relation creation/update time, UTС zone
        - is_active: bool | None

    Return:
    - List that contains the results of the query, serialized to
    the ItemRelation type
    """

    # query = tables.ItemRelation.objects()
    # for param, value in get_param.items():
    #     if value is not None:
    #         query = query.where(getattr(tables.ItemRelation, param, None) == value)
    # result = await query
    # return result

    query = tables.ItemRelation.objects()
    for param, value in get_param.items():
        if value is not None:
            # Розбиваємо параметр на частини
            parts = param.split("__")

            # Перевіряємо кількість частин
            if len(parts) == 1:
                # Якщо одна частина, просто використовуємо параметр
                query = query.where(getattr(tables.ItemRelation, param, None) == value)
            elif len(parts) == 2:
                # Якщо дві частини, використовуємо вкладений виклик
                nested_attr = getattr(tables.ItemRelation, parts[0], None)
                query = query.where(getattr(nested_attr, parts[1], None) == value)

    result = await query
    if not result:
        return []

    return result


async def update(id: UUID, **update_param: UpdateItemRelationRequest) -> UUID | None:
    """Update existing record in item relation.

    parameters:
    - id: UUID of item relation, required
    - customer: UUID of customer, used for ForeignKey links with Customer
    - context_1: UUID of context, used for ForeignKey links with Context
    - context_2: UUID of context, used for ForeignKey links with Context
    - last_date: item relation creation/update time, UTС zone
    - is_active: bool = True

    Return:
    - ItemRelation.id: UUID - primary key for new item relation record - UUID type
    - If there is no record with this id, it returns None

    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update item relation must be UUID-type, but got {type(id)}"
        )
    filtered_param = {k: v for k, v in update_param.items() if v is not None}
    result = (
        await tables.ItemRelation.update(filtered_param)
        .where(tables.ItemRelation.id == id)
        .returning(tables.ItemRelation.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete right_answ_item with right_answ_item.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_right_answ_item must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
