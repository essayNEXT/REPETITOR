from typing import Optional, List
from uuid import UUID

from pydantic import EmailStr
from asyncpg.exceptions import UniqueViolationError
from repetitor_backend.tables import Customer


async def get_customer(customer_id: UUID | int = None) -> List[Customer]:
    """
    Get existing customer according to match conditions:
    parameters:
    - customer_id: UUID|int:
        if customer_id == UUID - corresponds to the parameter tables.Customer.id
        if customer_id == int - corresponds to the parameter tables.Customer.tlg_user_id

    Returns a list that contains the results of the query, serialized to
    the Customer type, constructed as follows:
    SELECT *
    FROM customer
    WHERE
            customer.id = customer_id
    or
    SELECT *
    FROM customer
    WHERE
            customer.tlg_user_id = customer_id
    """
    if not isinstance(customer_id, (int, UUID)):
        raise TypeError(
            f"argument function 'get_customer' must be int or UUID, but gotten type {type(customer_id)}"
        )
    if isinstance(customer_id, int):
        qwery = Customer.objects().where(Customer.tlg_user_id == customer_id)
        result = await qwery
        return result
    elif isinstance(customer_id, UUID):
        qwery = Customer.objects().where(Customer.id == customer_id)
        result = await qwery
        return result


async def create_new_customer(
    customer_class: UUID,
    tlg_user_id: int,
    tlg_language: str,
    tlg_first_name: str,
    tlg_user_name: str = None,
    tlg_last_name: str = None,
    native_language: str = None,
    first_name: str = None,
    last_name: str = None,
    email: EmailStr = None,
) -> UUID | str:
    """Created a new customer.

    parameters:
    - customer_clas: UUID of customer class, used for ForeignKey links with CustomerType
    - tlg_user_id: BigInt(null=False, unique=True) - telegram_id of new customer
    - tlg_language: Varchar(lenght=10, null=False) - language of Telegram interface
    - tlg_user_name: Varchar(length=50, null=True) - username of customer in Telegram
    - tlg_first_name: Varchar(length=50, null=False) - first name of customer from Telegram
    - tlg_last_name: Varchar(length=50, null=True) - last name of customer from Telegram
    - native_language: Varchar(length=10, null=True) - native language of customer
    - first_name: Varchar(lenght=50, null=True) - real first name of customer
    - last_name: Varchar(lenght=50, null=True) - real last name of customer
    - email: Email(null=True) - email of customer
    result:
    - primary key for new customer record - UUID type
    - warning: str - in case of insert wrong data for create a new customer
    """
    try:
        result = await Customer.insert(
            Customer(
                customer_class=customer_class,
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
        return result[0]["id"]
    except UniqueViolationError:
        return f"A user with this ID ({tlg_user_id}) already exists"
    except IndexError:
        return f"There is no such user type ({customer_class})"


async def update_customer(
    id: UUID,
    customer_class: Optional[UUID] = None,
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
) -> None:
    """Update an existing customer.

    parameters:
    - id: UUID - primary key of customer record
    - customer_clas: UUID of customer class, used for ForeignKey links with CustomerType
    - tlg_user_id: BigInt(null=False, unique=True) - telegram_id of new customer
    - tlg_language: Varchar(lenght=10, null=False) - language of Telegram interface
    - tlg_user_name: Varchar(length=50, null=True) - username of customer in Telegram
    - tlg_first_name: Varchar(length=50, null=False) - first name of customer from Telegram
    - tlg_last_name: Varchar(length=50, null=True) - last name of customer from Telegram
    - native_language: Varchar(length=10, null=True) - native language of customer
    - first_name: Varchar(lenght=50, null=True) - real first name of customer
    - last_name: Varchar(lenght=50, null=True) - real last name of customer
    - email: Email(null=True) - email of customer
    - is_active: bool - activity state of customer

    Return None.
    """
    if not isinstance(id, UUID):
        raise TypeError(
            f"parameter 'id' for function update_context_type must be UUID-type, but got {type(id)}"
        )
    kwargs = {}
    update_values = [
        "customer_class",
        "tlg_user_id",
        "tlg_language",
        "tlg_first_name",
        "tlg_user_name",
        "tlg_last_name",
        "native_language",
        "first_name",
        "last_name",
        "email",
        "is_active",
    ]
    for value in update_values:
        if eval(value) is not None:
            kwargs[value] = eval(value)
    result = await Customer.update(**kwargs).where(Customer.id == id)
    return result if result else None


async def delete_customer(id: UUID) -> None:
    """
    Delete existing customer record.

    parameters:
    - id: UUID - primary key of customer record
    """
    result = await update_customer(id=id, is_active=False)
    return result
