import logging
from uuid import UUID
from .serializers import CustomerCreateRequest, CustomerUpdateRequest, CustomerResponse
from fastapi import APIRouter
from repetitor_backend.db.crud import customer
from typing import List

logger = logging.getLogger()

router = APIRouter()


@router.get("/customer")
async def get_customer(customer_id: UUID | int) -> List[CustomerResponse]:
    """
    Get list of Customer according to "query" parameter.

    Parameters:
    -customer_id: UUID|int
        if customer_id == UUID, corresponds to the parameter tables.Customer.id
        if customer_id == int, corresponds to the parameter tables.Customer.tlg_user_id

    Returns a list that contains the results of the query, serialized
    to the CustomerResponse type, constructed as follows:
    - if  customer_id == UUID:
        SELECT *
        FROM customer
        WHERE customer.id = customer_id

    - if if customer_id == int:
        SELECT *
        FROM customer
        WHERE customer.tlg_user_id = customer_id

    if customer_id parameter is missing in customer table records return an empty list.
    """
    results = await customer.get_customer(customer_id=customer_id)
    return [CustomerResponse.from_DB_model(db_model=result) for result in results]


@router.post("/customer")
async def create_customer(new_customer: CustomerCreateRequest) -> UUID:
    """
    Create a new customer.

    Parameters:
    - customer_clas: UUID of customer class, used for ForeignKey links with CustomerType
    - tlg_user_id: int - telegram_id of new customer, required
    - tlg_language: str, max lenght is 10 symbols - language of Telegram interface, required
    - tlg_user_name: str, max lenght is 50 symbols - username of customer in Telegram
    - tlg_first_name: str, max lenght is 50 symbols - first name of customer from Telegram, required
    - tlg_last_name: str, max lenght is 50 symbols - last name of customer from Telegram
    - native_language: str, max lenght is 10 symbols - native language of customer
    - first_name: str, max lenght is 50 symbols - real first name of customer
    - last_name: str, max lenght is 50 symbols - real last name of customer
    - email: str - email of customer

    Return:
    - Customer.id: UUID - primary key for new customer record - UUID type
    """
    return await customer.create_new_customer(
        customer_class=new_customer.customer_class,
        tlg_user_id=new_customer.tlg_user_id,
        tlg_language=new_customer.tlg_language,
        tlg_first_name=new_customer.tlg_first_name,
        tlg_user_name=new_customer.tlg_user_name,
        tlg_last_name=new_customer.tlg_last_name,
        native_language=new_customer.native_language,
        first_name=new_customer.first_name,
        last_name=new_customer.last_name,
        email=new_customer.email,
    )


@router.put("/customer")
async def update_customer(update_customer: CustomerUpdateRequest) -> UUID:
    """
    Update an existing customer record.

    Parameters:
    - id: UUID - primary key of customer record
    - customer_clas: UUID of customer class, used for ForeignKey links with CustomerType
    - tlg_user_id: int - telegram_id of new customer, required
    - tlg_language: str, max lenght is 10 symbols - language of Telegram interface, required
    - tlg_user_name: str, max lenght is 50 symbols - username of customer in Telegram
    - tlg_first_name: str, max lenght is 50 symbols - first name of customer from Telegram, required
    - tlg_last_name: str, max lenght is 50 symbols - last name of customer from Telegram
    - native_language: str, max lenght is 10 symbols - native language of customer
    - first_name: str, max lenght is 50 symbols - real first name of customer
    - last_name: str, max lenght is 50 symbols - real last name of customer
    - email: str - email of customer
    - is_active: bool - activity state of customer

    Return None.
    """
    return await customer.update_customer(
        id=update_customer.id,
        customer_class=update_customer.customer_class,
        tlg_user_id=update_customer.tlg_user_id,
        tlg_language=update_customer.tlg_language,
        tlg_first_name=update_customer.tlg_first_name,
        tlg_user_name=update_customer.tlg_user_name,
        tlg_last_name=update_customer.tlg_last_name,
        native_language=update_customer.native_language,
        first_name=update_customer.first_name,
        last_name=update_customer.last_name,
        email=update_customer.email,
        is_active=update_customer.is_active,
    )


@router.delete("/customer")
async def delete_customer(id: UUID) -> UUID:
    """
    Delete an existing customer record.

    Parameters:
    - id: UUID - primary key of customer record

    Return None.
    """
    return await customer.update_customer(id=id, is_active=False)
