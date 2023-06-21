from uuid import UUID

from repetitor_backend import tables
from repetitor_backend.api.v1.context.serializers import (
    GetContextRequest,
    UpdateContextRequest,
    ContextCreateRequest,
)


async def create(**kwargs: ContextCreateRequest) -> UUID:
    """Create new context.

    parameters:

    """
    result = await tables.Context.insert(tables.Context(**kwargs)).returning(
        tables.Context.id
    )
    return result[0]["id"]


async def get(**get_param: GetContextRequest) -> list[tables.Context]:
    """Get a list of existing contexts according to match conditions:"""
    query = (
        tables.Context.objects()
    )  # .where(tables.Context.is_active == get_param.is_active)
    for param, value in get_param.items():
        if value is not None:
            if param == "description":
                query = query.where(
                    tables.Context.description.like("%" + str(value) + "%")
                )
            else:
                query = query.where(getattr(tables.Context, param, None) == value)
    result = await query
    return result


async def update(id: UUID, **update_param: UpdateContextRequest) -> UUID | None:
    """Update existing record in context.

    parameters:

    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update_item must be UUID-type, but got {type(id)}"
        )
    filtered_param = {k: v for k, v in update_param.items() if v is not None}
    result = (
        await tables.Context.update(filtered_param)
        .where(tables.Context.id == id)
        .returning(tables.Context.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete context with context.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type. If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_context must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
