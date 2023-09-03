from uuid import UUID
from typing import Optional, List

from fastapi import HTTPException

from repetitor_backend.tables import CustomerType


async def create_new_customer_type(name: str, description: str) -> UUID:
    """Created a new customer type.

    parameters:
    - name (Varchar(50), unique) - short name of customer type, required
    - description (Varchar(200)) - description of customer type
    result:
    - primary key for new record - UUID type
    """
    if not (isinstance(name, str) and isinstance(description, str)):
        raise TypeError(
            f"paremeter 'name' and 'description' for customer_type must be only\
str-type, but type(name)={type(name)} and type(description)={type(description)}"
        )
    elif not (len(name) <= 50 and len(description) <= 200):
        raise HTTPException(
            status_code=404,
            detail=f"len(name) must be <= 50 and len(description) must be <= 200, but\
got len(name)={len(name)} and len(description)={len(description)}",
        )
    result = await CustomerType.insert(
        CustomerType(name=name, description=description)
    ).returning(CustomerType.id)
    return result[0]["id"]


async def get_customer_type(
    id: Optional[UUID] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = True,
) -> List[CustomerType]:
    """Get a list of existing customer_tyupes according to match conditions:

    id: UUID, corresponds to the parameter tables.CustomerType.id
    name: str, corresponds to the parameter tables.CustomerType.name
    describe: str, corresponds to the parameter tables.CustomerType.describe
    is_active: bool, corresponds to the parameter tables.CustomerType.is_active

    Returns a list that contains the results of the query, serialized to
    the CustomerTypeResponce type, constructed as follows:
    SELECT *
    FROM customer_type
    WHERE
            customer_type.id = id
        AND customer_type.name = name
        AND customer_type.describe LIKE '%describe%'
        AND customer_type.is_active = is_active;

    if some parameter is None (as id, name, describe) - the corresponding line
    in the request is simply missing
    """
    query = CustomerType.objects().where(CustomerType.is_active == is_active)
    if id:
        query = query.where(CustomerType.id == id)
    if name:
        query = query.where(CustomerType.name == name)
    if description:
        query = query.where(CustomerType.description.like("%" + description + "%"))
    result = await query
    return result
