import aiohttp


async def get_customer_type(customer_type_name: str) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://repetitor_backend/api/v1/type/customer/"
        ) as response:
            customer_types = await response.json()
            for customer_type in customer_types:
                if customer_type["name"] == customer_type_name:
                    return customer_type
        return None
