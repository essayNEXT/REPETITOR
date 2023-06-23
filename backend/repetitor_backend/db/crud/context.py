from uuid import UUID

from repetitor_backend import tables
from repetitor_backend.api.v1.context.serializers import (
    GetContextRequest,
    UpdateContextRequest,
    ContextCreateRequest,
)


async def create(**kwargs: ContextCreateRequest) -> UUID:
    """Create new item.
    Parameters:
        - name: str, max lenght is 50 symbols - the name of the context, required
        - name_short: str, max lenght is 10 symbols - the short name of the context, required
        - context_class: UUID of context, used for ForeignKey links with Context, required
        - description: str, max lenght is 255 symbols - context description, required
        - is_active: bool = True
    Return:
    - Item.id: UUID - primary key for new item record - UUID type
    """
    result = await tables.Context.insert(tables.Context(**kwargs)).returning(
        tables.Context.id
    )
    return result[0]["id"]


async def get(**get_param: GetContextRequest) -> list[tables.Context]:
    """Get a list of existing item according to match conditions:
        Parameters:
        - id: UUID of item
        - name: str, max lenght is 50 symbols - the name of the context
        - name_short: str, max lenght is 10 symbols - the short name of the context
        - context_class: UUID of context, used for ForeignKey links with Context
        - description: str, max lenght is 255 symbols - context description
        - is_active: bool = True
    Return:
    - List that contains the results of the query
    """
    query = tables.Context.objects()
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
    """Update existing record in customer context.

    parameters:
        - id: UUID of item
        - name: str, max lenght is 50 symbols - the name of the context
        - name_short: str, max lenght is 10 symbols - the short name of the context
        - context_class: UUID of context, used for ForeignKey links with Context
        - description: str, max lenght is 255 symbols - context description
        - is_active: bool = True
    Return:
    - CustomerContext.id: UUID - primary key for new customer context record - UUID type
    - If there is no record with this id, it returns None
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
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_context must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
