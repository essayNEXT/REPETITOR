from uuid import UUID
from repetitor_backend.tables import Customer


async def get_customer(customer_id: UUID | int):
    """
    Get existing customer according to match conditions:

    If id == UUID then id: UUID, corresponds to the parameter tables.Customer.id
    If id == int then id: int, corresponds to the parameter tables.Customer.tlg_user_id

    """
    if not isinstance(customer_id, (int, UUID)):
        raise TypeError(
            f"argument function 'get_customer' must be int or UUID, but goten type {type(customer_id)}"
        )
    if isinstance(customer_id, int):
        qwery = Customer.objects().where(Customer.tlg_user_id == customer_id)
        result = await qwery
    if isinstance(customer_id, UUID):
        qwery = Customer.objects().where(Customer.id == customer_id)
        result = await qwery
    return result
