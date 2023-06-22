from uuid import UUID
from typing import Optional, List
from repetitor_backend import tables


async def create(name: str, description: str) -> UUID:
    """Create new context type.

    parameters:
    - name (Varchar(50), unique) - short name of customer type, required
    - description (Varchar(200)) - description of customer type
    result:
    - primary key for new record - UUID type
    """

    if not (isinstance(name, str) and isinstance(description, str)):
        raise TypeError(
            f"paremeter 'name' and 'description' for context_type must be only\
str-type, but type(name)={type(name)} and type(description)={type(description)}"
        )
    elif not len(name) <= 20:
        raise ValueError(f"len(name) must be <= 20, but got len(name)={len(name)}")
    result = await tables.ContextType.insert(
        tables.ContextType(name=name, description=description)
    ).returning(tables.ContextType.id)
    return result[0]["id"]


async def get(
    id: Optional[UUID] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = True,
) -> List[tables.ContextType]:
    """Get a list of existing context_types according to match conditions:

    id: UUID, corresponds to the parameter tables.ContextType.id
    name: str, corresponds to the parameter tables.ContextType.name
    describe: str, corresponds to the parameter tables.ContextType.describe
    is_active: bool, corresponds to the parameter tables.ContextType.is_active

    Returns a list that contains the results of the query, constructed as follows:
    SELECT *
    FROM context_type
    WHERE
            context_type.id = id
        AND context_type.name = name
        AND context_type.description LIKE '%description%'
        AND context_type.is_active = is_active;

    if some parameter is None (as id, name, description) - the corresponding line
    in the request is simply missing
    """
    query = tables.ContextType.objects().where(
        tables.ContextType.is_active == is_active
    )
    if id:
        query = query.where(tables.ContextType.id == id)
    if name:
        query = query.where(tables.ContextType.name == name)
    if description:
        query = query.where(
            tables.ContextType.description.like("%" + description + "%")
        )
    result = await query
    return result


async def update(
    id: UUID,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> UUID | None:
    """Update existing record in context_table.

    parameters:
    id: UUID, required
    name: str, optional. len(name) <= 20 (if more then 20 raise ValueError)
    description: str, optional
    is_active: bool, optopnal.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update_context_type must be UUID-type, but got {type(id)}"
        )
    kwargs = {}
    if name is not None:
        if not isinstance(name, str):
            raise TypeError(
                f"parameter 'name' for function update_context_type must be str-type, but got {type(name)}"
            )
        if len(name) > 20:
            raise ValueError(
                f"the 'name' parameter must be no more than 20 characters long, received {len(name)}"
            )
        kwargs["name"] = name
    if description is not None:
        if not isinstance(description, str):
            raise TypeError(
                f"parameter 'description' for function update_context_type must be str-type, but got {type(description)}"
            )
        kwargs["description"] = description
    if is_active is not None:
        if not isinstance(is_active, bool):
            raise TypeError(
                f"parameter 'is_active' for function update_context_type must be bool-type, but got {type(is_active)}"
            )
        kwargs["is_active"] = is_active
    result = (
        await tables.ContextType.update(**kwargs)
        .where(tables.ContextType.id == id)
        .returning(tables.ContextType.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete context_type with context_type.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type. If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_context_type must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
