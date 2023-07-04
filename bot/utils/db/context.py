import aiohttp


async def get_context():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://repetitor_backend/api/v1/context/") as response:
            context = await response.json()
            return context


async def get_context_by_short_name(short_name: str):
    async with aiohttp.ClientSession() as session:
        url = "http://repetitor_backend/api/v1/context/"
        params = {"name_short": short_name}
        async with session.get(url, params=params) as response:
            context = await response.json()
            return context
