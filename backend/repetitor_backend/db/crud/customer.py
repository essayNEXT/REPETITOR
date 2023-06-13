from uuid import UUID

from pydantic import EmailStr

from repetitor_backend.tables import Customer
from repetitor_backend.db.crud.customertype import get_customer_type


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


async def create_new_customer(
        customer_class: str,
        tlg_user_id: int,
        tlg_language: str,
        tlg_first_name: str,
        tlg_user_name: str = None,
        tlg_last_name: str = None,
        native_language: str = None,
        first_name: str = None,
        last_name: str = None,
        email: EmailStr = None

):
    customer_uuid = get_customer_type(name=customer_class)
    result = await Customer.insert(
        Customer(
            customer_class=customer_uuid[0].id,
            tlg_user_id=tlg_user_id,
            tlg_language=tlg_language,
            tlg_user_name=tlg_user_name,
            tlg_first_name=tlg_first_name,
            tlg_last_name=tlg_last_name,
            first_name=first_name,
            native_language=native_language,
            last_name=last_name,
            email=email,
        ))
    return result
