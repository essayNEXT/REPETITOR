from repetitor_backend.external_api.microsoft_v2 import translate
import asyncio
import aiohttp


async def test_microsoft():
    async with aiohttp.ClientSession() as session:
        result = await translate(session, "uk", "en", "додати")
    print(result)


if __name__ == "__main__":
    asyncio.run(test_microsoft())

# запуск тесту з папки REPETITOR\backend , в командному рядку ввести
# python -m tests.test_microsoft
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
# https://ru.stackoverflow.com/questions/1089222/importerror-attempted-relative-import-with-no-known-parent-package-python
