from uuid import UUID
from repetitor_backend.tables import CustomerType


async def create_new_customer_type(
        name: str,
        description: str
) -> UUID:
    result = await CustomerType.insert(
        CustomerType(name=name, description=description)
    ).returning(CustomerType.id)
    return result[0]["id"]
