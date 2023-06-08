import asyncio
from uuid import UUID
from typing import Optional, List
from repetitor_backend import tables


async def create(
        name: str,
        description: str
) -> UUID:
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
        raise ValueError(
            f"len(name) must be <= 20, but got len(name)={len(name)}"
        )
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
    query = tables.ContextType.objects().where(tables.ContextType.is_active == is_active)
    if id:
        query = query.where(tables.ContextType.id == id)
    if name:
        query = query.where(tables.ContextType.name == name)
    if description:
        query = query.where(tables.ContextType.description.like("%" + description + "%"))
    result = await query
    return result


async def update(
        id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None
) -> UUID | None:
    """Update existing record in context_table.

    parameters:
    id: UUID, required
    name: str, optional. len(name) <= 20 (if more then 20 raise ValueError)
    description: str, optional
    is_active: bool, optopnal.
    """
    if not isinstance(id, UUID):
        raise TypeError(f"parameter 'id' for function update_context_type must be UUID-type, but got {type(id)}")
    kwargs = {}
    if name is not None:
        if not isinstance(name, str):
            raise TypeError(f"parameter 'name' for function update_context_type must be str-type, but got {type(name)}")
        if len(name) > 20:
            raise ValueError(f"the 'name' parameter must be no more than 20 characters long, received {len(name)}")
        kwargs["name"] = name
    if description is not None:
        if not isinstance(description, str):
            raise TypeError(f"parameter 'description' for function update_context_type must be str-type, but got {type(description)}")
        kwargs["description"] = description
    if is_active is not None:
        if not isinstance(is_active, bool):
            raise TypeError(f"parameter 'is_active' for function update_context_type must be bool-type, but got {type(is_active)}")
        kwargs["is_active"] = is_active
    result = await tables.ContextType.update(**kwargs).where(tables.ContextType.id == id).returning(tables.ContextType.id)
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
        raise TypeError(f"parameter 'id' for function del_context_type must be UUID-type, but got {type(id)}")
    result = await update(id=id, is_active=False)
    return result


if __name__ == "__main__":

    async def test_crud_context_type() -> None:
        # only for simply testing
        # create new context type
        NAME = "test_language"
        DESCRIPTION = "it is testing context_type record"
        NAME_NEW = "test_lng"
        DESCRIPTION_NEW = "a new description for the update function testing"
        id_test_record = await create(name=NAME, description=DESCRIPTION)
        assert isinstance(id_test_record, UUID), f"during the creation \
            test context_tupe record got wrong id: {id_test_record}"
        print(f"id_test_record: {id_test_record}")
        # get list of existing context_types
        context_types_for_id = await get(id=id_test_record)
        assert context_types_for_id[0].id == id_test_record, f"contexttype.get(id=existing_id)\
            returned wrong result: {context_types_for_id}"
        print(f"get for id={id_test_record} --> {context_types_for_id}")
        context_types_for_NAME = await get(name=NAME)
        assert context_types_for_NAME[0].id == id_test_record, f"contexttype.get(name=existing_name)\
            returned wrong result: {context_types_for_NAME}"
        print(f"get for name={NAME} --> {context_types_for_NAME}")
        context_types_for_DESCRIPTION = await get(description=DESCRIPTION[:-3])
        assert context_types_for_DESCRIPTION[0].id == id_test_record, f"contexttype.get(description=existing_description)\
            returned wrong result: {context_types_for_DESCRIPTION}"
        print(f"get for description={DESCRIPTION[:-3]} --> {context_types_for_DESCRIPTION}")
        # update existing context_type
        id_after_update = await update(id=id_test_record, name=NAME_NEW, description=DESCRIPTION_NEW)
        assert id_after_update == id_test_record,  f"contexttype.update(id=existing_id, \
            name=NAME_NEW, description=DESCRIPTION_NEW) returned wrong result: {id_after_update}"
        print(f"await update(id={id_test_record}, name={NAME_NEW}, description={DESCRIPTION_NEW}) returned {id_after_update}")
        # get an updated record
        updated_record = (await get(id=id_after_update))[0]
        assert updated_record.description == DESCRIPTION_NEW, f"contexttype.get(id=id_after_update), \
            returned wrong result: {updated_record}"
        print(f"record after update: {updated_record}")
        # test for delete
        id_after_delete = await delete(id=id_test_record)
        assert id_after_delete == id_test_record, f"contexttype.delete(id={id_test_record})\
            returned wrong id: {id_after_delete}"
        print(f"await delete(id={id_test_record}) returned {id_after_delete}")
        deleted_record = (await get(id=id_test_record, is_active=False))[0]
        assert deleted_record.id == id_test_record and deleted_record.is_active == False, f"\
            contexttype.get(id={id_test_record}, is_active=False) returned wrong record: {deleted_record}"
        print(f"deleted_record: {deleted_record}")

    asyncio.run(test_crud_context_type())
