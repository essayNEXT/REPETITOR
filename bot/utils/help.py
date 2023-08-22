from abc import abstractmethod, ABC
from asyncinit import asyncinit
import aiohttp


@asyncinit
class HelpConstructor(ABC):
    HELP_URL = "http://repetitor_backend/api/v1/help/"

    async def __init__(self):
        # for help_message in self.help_messages:
        #     result = await self.__get_help_message(help_message)
        #     if result is None:
        #         await self.__post_help_message(help_message)
        pass

    async def __get_help_message(self, help_message) -> list | None:
        async with aiohttp.ClientSession() as session:
            params = help_message
            async with session.get(self.HELP_URL, params=params) as response:
                help_from_db = await response.json()
                return help_from_db

    async def __post_help_message(self, help_message) -> list | None:
        async with aiohttp.ClientSession() as session:
            data = help_message
            async with session.post(self.HELP_URL, json=data) as response:
                help_from_db = await response.json()
                return help_from_db

    @property
    @abstractmethod
    def help_messages(self):
        pass
