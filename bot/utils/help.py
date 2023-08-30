from abc import abstractmethod, ABC
from asyncinit import asyncinit
from typing_extensions import TypedDict
from pydantic import TypeAdapter, ValidationError
import aiohttp


class HelpConstructor(ABC):
    @staticmethod
    @abstractmethod
    def help_messages() -> list[dict]:
        pass


class HelpMessageDict(TypedDict):
    state_name: str
    language_code: str
    help_text: str


@asyncinit
class HelpPublisher:
    HELP_URL = "http://repetitor_backend/api/v1/help/"

    async def __init__(self, kb_classes: list):
        self.help_messages_to_db = [
            {
                "state_name": "No_Telegram_state",
                "language_code": "en",
                "help_text": "Do anything you want now. Here some of commands and possibilities: ...",
            }
        ]

        # Перебираємо список класів Клавіатури та витягуємо з них параметри help_messages
        for kb_class in kb_classes:
            self.help_messages_to_db += kb_class.help_messages()

        for help_message in self.help_messages_to_db:
            if self.help_message_validator(help_message):
                print(f"Help for {help_message['state_name']} is correct!")
                # result = await self.__get_help_message(help_message)
                # if result is None:
                #     await self.__post_help_message(help_message)
        print(self.help_messages_to_db)

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

    @staticmethod
    def help_message_validator(help_message_dict: dict):
        """Функція повинна перевіряти структуру та правильність заповнення параметра help_messages"""
        ta = TypeAdapter(HelpMessageDict)
        try:
            ta.validate_python(help_message_dict)
            return True
        except ValidationError as err:
            print(f"{err} - Wrong structure of help!")
            return False
