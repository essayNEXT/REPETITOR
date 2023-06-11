from repetitor_backend.external_api.microsoft import translate
import asyncio


async def test_microsoft():
    result = await translate("uk", "en", "додати")
    print(result)


if __name__ == "__main__":
    asyncio.run(test_microsoft())
