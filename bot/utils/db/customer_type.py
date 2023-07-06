import aiohttp


async def get_customer_type(customer_type_name: str) -> dict | None:
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/type/customer/"
        params = {"name": customer_type_name}
        async with session.get(url, params=params) as response:
            customer_types = await response.json()
            return customer_types[0]
