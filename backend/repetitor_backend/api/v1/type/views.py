import logging

from typing import List
from uuid import UUID
from fastapi import APIRouter

from .serializers import CustomerTypeCreateRequest
from repetitor_backend.db.crud import customertype



logger = logging.getLogger()

router = APIRouter()


@router.post("/type/customer/")
async def create_customer_type(new_customer_type: CustomerTypeCreateRequest) -> UUID:
    """Create a new class of customer.
    
    Parameters:
    - name: str, max lenght is 50 symbols, required
    - describe: str, max lenght is 200 symbols, required
    """
    return await customertype.create_new_customer_type(
        name=new_customer_type.name,
        description=new_customer_type.description
    )



# @router.get("/type/customer/")
# async def get_customer_type(
#     id: UUID | None = None,
#     name: str | None = None,
#     describe: str | None = None,
#     is_active: bool = True
# ) -> List[CustomerTypeResponce | None]:
#     """Get list of Customer Type according of "query" parameter.

#     id: UUID, corresponds to the parameter tables.CustomerType.id
#     name: str, corresponds to the parameter tables.CustomerType.name
#     describe: str, corresponds to the parameter tables.CustomerType.describe
#     is_active: bool, corresponds to the parameter tables.CustomerType.is_active

#     Returns a list that contains the results of the query, serialized to
#     the CustomerTypeResponce type, constructed as follows:
#     SELECT *
#     FROM customer_type
#     WHERE
#             customer_type.id = id
#         AND customer_type.name = name
#         AND customer_type.describe LIKE '%describe%'
#         AND customer_type.is_active = is_active;
    
#     if some parameter is None (as id, name, describe) - the corresponding line
#     in the request is simply missing
#     """
#     return {"Hello": "World"}
