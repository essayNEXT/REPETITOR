"""
Test for CRUD operations with context_type, DB level.

This is a simple test for manual running and manual testing. For
automated testing, it needs to be improved.
"""

import asyncio
from uuid import UUID
from repetitor_backend.db.crud.contexttype import get, create, update, delete


async def test_crud_context_type() -> None:
    # only for simply testing
    # create new context type
    NAME = "test_language"
    DESCRIPTION = "it is testing context_type record"
    NAME_NEW = "test_lng"
    DESCRIPTION_NEW = "a new description for the update function testing"
    id_test_record = await create(name=NAME, description=DESCRIPTION)
    assert isinstance(
        id_test_record, UUID
    ), f"during the creation \
        test context_tupe record got wrong id: {id_test_record}"
    print(f"id_test_record: {id_test_record}")
    # get list of existing context_types
    context_types_for_id = await get(id=id_test_record)
    assert (
        context_types_for_id[0].id == id_test_record
    ), f"contexttype.get(id=existing_id)\
        returned wrong result: {context_types_for_id}"
    print(f"get for id={id_test_record} --> {context_types_for_id}")
    context_types_for_NAME = await get(name=NAME)
    assert (
        context_types_for_NAME[0].id == id_test_record
    ), f"contexttype.get(name=existing_name)\
        returned wrong result: {context_types_for_NAME}"
    print(f"get for name={NAME} --> {context_types_for_NAME}")
    context_types_for_DESCRIPTION = await get(description=DESCRIPTION[:-3])
    assert (
        context_types_for_DESCRIPTION[0].id == id_test_record
    ), f"contexttype.get(description=existing_description)\
        returned wrong result: {context_types_for_DESCRIPTION}"
    print(f"get for description={DESCRIPTION[:-3]} --> {context_types_for_DESCRIPTION}")
    # update existing context_type
    id_after_update = await update(
        id=id_test_record, name=NAME_NEW, description=DESCRIPTION_NEW
    )
    assert (
        id_after_update == id_test_record
    ), f"contexttype.update(id=existing_id, \
        name=NAME_NEW, description=DESCRIPTION_NEW) returned wrong result: {id_after_update}"
    print(
        f"await update(id={id_test_record}, name={NAME_NEW}, description={DESCRIPTION_NEW}) returned {id_after_update}"
    )
    # get an updated record
    updated_record = (await get(id=id_after_update))[0]
    assert (
        updated_record.description == DESCRIPTION_NEW
    ), f"contexttype.get(id=id_after_update), \
        returned wrong result: {updated_record}"
    print(f"record after update: {updated_record}")
    # test for delete
    id_after_delete = await delete(id=id_test_record)
    assert (
        id_after_delete == id_test_record
    ), f"contexttype.delete(id={id_test_record})\
        returned wrong id: {id_after_delete}"
    print(f"await delete(id={id_test_record}) returned {id_after_delete}")
    deleted_record = (await get(id=id_test_record, is_active=False))[0]
    assert (
        deleted_record.id == id_test_record and deleted_record.is_active is False
    ), f"\
        contexttype.get(id={id_test_record}, is_active=False) returned wrong record: {deleted_record}"
    print(f"deleted_record: {deleted_record}")


asyncio.run(test_crud_context_type())
