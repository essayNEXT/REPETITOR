from datetime import datetime
from uuid import UUID

from asyncpg import ForeignKeyViolationError

from repetitor_backend import tables
from repetitor_backend.api.v1.customer_context.serializers import (
    GetCustomerContextRequest,
    UpdateCustomerContextRequest,
    CustomerContextCreateRequest,
)

CONTEXT_TYPE_NAME_FOR_BIDIRECTIONAL = "language"


async def create(**kwargs: CustomerContextCreateRequest | datetime) -> UUID | str:
    """Create new customer context.
    Parameters:
        - customer: UUID of customer, used for ForeignKey links with Customer, required
        - context_1: UUID of context, used for ForeignKey links with Context, required
        - context_2: UUID of context, used for ForeignKey links with Context, required

    Return:
    - CustomerContext.id: UUID - primary key for new customer context record - UUID type
    - str - error message in case of invalid foreign keys
    """

    # kwargs["is_active"] = None
    check_exists = await get(
        **kwargs
    ) or await bidirectional_context_for_a_language_context_type(**kwargs)

    if check_exists:  # якщо існує  такий запис
        return (
            f"an object with such parameters already exists id={check_exists[0].id}  "
            f"is_active={check_exists[0].is_active} "
        )
        raise TypeError(
            f"an object with such parameters already exists {check_exists[0].id}"
        )

    kwargs["last_date"] = datetime.utcnow()
    try:
        result = await tables.CustomerContext.insert(
            tables.CustomerContext(**kwargs)
        ).returning(tables.CustomerContext.id)
    except ForeignKeyViolationError as e:
        return str(e)
    return result[0]["id"]


async def bidirectional_context_for_a_language_context_type(
    **get_param: GetCustomerContextRequest,
) -> list[tables.CustomerContext] | None:
    """checking contexts when creating a user context. bidirectionality check when the user context is created,
    if the context type is context_1=="language". if true, prevents the creation of duplicates in the user context.
    problem solving (customer, context_1, context_2) == (customer, context_2, context_1):

        Parameters:
        - id: UUID of customer context
        - customer: UUID of customer, used for ForeignKey links with Customer
        - context_1: UUID of context, used for ForeignKey links with Context
        - context_2: UUID of context, used for ForeignKey links with Context

    Return:
    - List that contains the results of the query, serialized to the CustomerContext type
    """

    query = tables.CustomerContext.objects()
    query = query.where(
        (tables.CustomerContext.customer == get_param["customer"])
        & (
            tables.CustomerContext.context_1.context_type.name
            == CONTEXT_TYPE_NAME_FOR_BIDIRECTIONAL
        )
        & (tables.CustomerContext.context_2 == get_param["context_1"])
        & (tables.CustomerContext.context_1 == get_param["context_2"])
    )
    result = await query
    return result


async def get(**get_param: GetCustomerContextRequest) -> list[tables.CustomerContext]:
    """Get a list of existing customer context according to match conditions:
        Parameters:
        - id: UUID of customer context
        - customer: UUID of customer, used for ForeignKey links with Customer
        - context_1: UUID of context, used for ForeignKey links with Context
        - context_2: UUID of context, used for ForeignKey links with Context
        - last_date: customer context creation/update time, UTС zone
        - is_active: bool | None

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


async def get_the_latest_context_based_on_customer_tg_id(
    customer_tg_id: UUID | int,
) -> dict:
    """
    Get the latest context based on id or tg_id in extended format:
        Parameters:
        - customer_tg_id: UUID|int, required
            - if customer_tg_id == UUID, corresponds to the parameter tables.Customer.id
            - if customer_tg_id == int, corresponds to the parameter tables.Customer.tlg_user_id

    Return:
    - Dict that contains the results of the query:
        context_1_id_sn: tuple(id, name_short)
        context_2_id_sn: tuple(id, name_short),
        author: UUID, corresponds to the parameter tables.Customer.id
    """
    query = tables.CustomerContext.objects().where(
        tables.CustomerContext.is_active.eq(True)
    )
    if isinstance(customer_tg_id, UUID):
        query = query.where(tables.CustomerContext.customer == customer_tg_id)
    elif isinstance(customer_tg_id, int):
        query = query.where(
            tables.CustomerContext.customer.tlg_user_id == customer_tg_id
        )
    else:
        raise TypeError(
            f"argument function 'get_context_on_customer_id' must be int or UUID,but gotten type {type(customer_tg_id)}"
        )

    query = query.order_by(tables.CustomerContext.last_date, ascending=False).first()
    result_all_fk = await query.prefetch(tables.CustomerContext.all_related())
    return dict(
        context_1_id_sn=(
            result_all_fk.context_1.id,
            result_all_fk.context_1.name_short,
        ),
        context_2_id_sn=(
            result_all_fk.context_2.id,
            result_all_fk.context_2.name_short,
        ),
        author=result_all_fk.customer.id,
    )


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
            f"parameter 'id' for function update customer context must be UUID-type, but got {type(id)}"
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
