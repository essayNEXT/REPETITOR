from ..repetitor_backend.external_api.microsoft import translate
import asyncio

loop = asyncio.get_event_loop()
loop.run_until_complete(translate("en", "uk", "my dog's name is Lucky"))

# res = translate("en", "ua", "my dog's name is Lucky")
# print(res)