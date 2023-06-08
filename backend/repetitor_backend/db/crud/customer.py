from uuid import UUID

# from repetitor_backend.tables import Customer, CustomerType


async def get_customer(id: int | UUID) -> dict | None:
    if not isinstance(id, (int, UUID)):
        raise TypeError(
            f"argument function 'get_customer' must be int or UUID, but goten type {type(id)}"
        )
    elif isinstance(id, int):
        pass  # int
    pass  # UUID
