from repetitor_backend.external_api.microsoft import translate_lng
import asyncio
import json


async def test_microsoft_lng():
    result = await translate_lng("uk")

    # словник підтримуваних мов
    print(
        json.dumps(
            result, sort_keys=True, ensure_ascii=False, indent=4, separators=(",", ": ")
        )
    )

    # список підтримуваних мов
    res = [key for key in result]
    print(res)
    print(len(res))


if __name__ == "__main__":
    asyncio.run(test_microsoft_lng())

# запуск тесту з папки REPETITOR\backend , в командному рядку ввести
# python -m tests.test_microsoft
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
# https://ru.stackoverflow.com/questions/1089222/importerror-attempted-relative-import-with-no-known-parent-package-python
