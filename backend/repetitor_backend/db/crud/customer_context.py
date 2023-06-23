from datetime import datetime
from uuid import UUID

from repetitor_backend import tables
from repetitor_backend.api.v1.customer_context.serializers import (
    GetCustomerContextRequest,
    UpdateCustomerContextRequest,
    CustomerContextCreateRequest,
)


async def create(**kwargs: CustomerContextCreateRequest | datetime) -> UUID:
    """Create new customer context.
    Parameters:
        - customer: UUID of customer, used for ForeignKey links with Customer, required
        - context_1: UUID of context, used for ForeignKey links with Context, required
        - context_2: UUID of context, used for ForeignKey links with Context, required
        - last_date: customer context creation time, UTС zone
        - is_active: bool = True

    Return:
    - CustomerContext.id: UUID - primary key for new customer context record - UUID type
    """

    # kwargs["last_date"] = None
    # check_exists = await get(**kwargs)
    kwargs["last_date"] = datetime.utcnow()
    # if check_exists:  # якщо існує  такий запис
    #     return await update(id=check_exists[0].id, **kwargs)

    result = await tables.CustomerContext.insert(
        tables.CustomerContext(**kwargs)
    ).returning(tables.CustomerContext.id)
    return result[0]["id"]


async def get(**get_param: GetCustomerContextRequest) -> list[tables.CustomerContext]:
    """Get a list of existing customer context according to match conditions:
        Parameters:
        - id: UUID of customer context
        - customer: UUID of customer, used for ForeignKey links with Customer
        - context_1: UUID of context, used for ForeignKey links with Context
        - context_2: UUID of context, used for ForeignKey links with Context
        - last_date: customer context creation/update time, UTС zone
        - is_active: bool = True

    Return:
    - List that contains the results of the query, serialized to
    the CustomerContext type
    """
    query = tables.CustomerContext.objects()
    for param, value in get_param.items():
        if value is not None:
            query = query.where(getattr(tables.CustomerContext, param, None) == value)
    result = await query
    return result


async def update(id: UUID, **update_param: UpdateCustomerContextRequest) -> UUID | None:
    """Update existing record in customer context.

    parameters:
    - id: UUID of customer context, required
    - customer: UUID of customer, used for ForeignKey links with Customer
    - context_1: UUID of context, used for ForeignKey links with Context
    - context_2: UUID of context, used for ForeignKey links with Context
    - last_date: customer context creation/update time, UTС zone
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
        await tables.CustomerContext.update(filtered_param)
        .where(tables.CustomerContext.id == id)
        .returning(tables.CustomerContext.id)
    )
    return result[0]["id"] if result else None


async def delete(id: UUID) -> UUID | None:
    """Delete customer_context with customer_context.id == id.

    parameter:
    - id - UUID.
    result:
    - primary key for deleted record - UUID type.
    - If there is no record with this id, it returns None.

    If parameter has wrong type - raise TypeError.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function del_customer_context must be UUID-type, but got {type(id)}"
        )
    result = await update(id=id, is_active=False)
    return result
