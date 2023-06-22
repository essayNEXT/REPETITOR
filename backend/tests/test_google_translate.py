"""
Test for google translate function.
"""

import asyncio
from repetitor_backend.external_api.google import translate


async def test_translate() -> None:
    # simply test: source
    result = await translate(target="EN", text="додати")
    print(result)


asyncio.run(test_translate())
