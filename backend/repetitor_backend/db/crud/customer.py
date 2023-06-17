from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from asyncpg.exceptions import UniqueViolationError
from repetitor_backend.tables import Customer
from repetitor_backend.db.crud.customertype import get_customer_type


async def get_customer(customer_id: UUID | int = None):
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
    email: EmailStr = None,
):
    try:
        customer_uuid = await get_customer_type(name=customer_class)
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
            )
        )
        return result
    except UniqueViolationError:
        return f"A user with this ID ({tlg_user_id}) already exists"
    except IndexError:
        return f"There is no such user type ({customer_class})"


async def update_customer(
    id: UUID,
    customer_class: Optional[str] = None,
    tlg_user_id: Optional[int] = None,
    tlg_language: Optional[str] = None,
    tlg_first_name: Optional[str] = None,
    tlg_user_name: Optional[str] = None,
    tlg_last_name: Optional[str] = None,
    native_language: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[EmailStr] = None,
    is_active: Optional[bool] = None,
):
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update_context_type must be UUID-type, but got {type(id)}"
        )
    kwargs = {}
    # if customer_class is not None:
    #     kwargs["customer_class"] = customer_class
    # if tlg_user_id is not None:
    #     kwargs["tlg_user_id"] = tlg_user_id
    # if tlg_language is not None:
    #     kwargs["tlg_language"] = tlg_language
    # if tlg_first_name is not None:
    #     kwargs["tlg_first_name"] = tlg_first_name
    # if tlg_user_name is not None:
    #     kwargs["tlg_user_name"] = tlg_user_name
    # if tlg_last_name is not None:
    #     kwargs["tlg_last_name"] = tlg_last_name
    # if native_language is not None:
    #     kwargs["native_language"] = native_language
    # if first_name is not None:
    #     kwargs["first_name"] = first_name
    # if last_name is not None:
    #     kwargs["last_name"] = last_name
    # if email is not None:
    #     kwargs["email"] = email
    # if is_active is not None:
    #     kwargs["is_active"] = is_active
    result = await Customer.update(**kwargs).where(Customer.id == id)
    return result if result else None


async def delete_customer(id: UUID, is_active: bool):
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update_context_type must be UUID-type, but got {type(id)}"
        )
    result = Customer.update({Customer.id: is_active}).where(Customer.id == id)
    return result
