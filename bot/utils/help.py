from abc import abstractmethod, ABC
from asyncinit import asyncinit
from typing_extensions import TypedDict
from pydantic import TypeAdapter, ValidationError
import aiohttp
from .db.context import get_context_by_short_name


class HelpConstructor(ABC):
    @staticmethod
    @abstractmethod
    def help_messages() -> list[dict]:
        pass


class HelpMessageDict(TypedDict):
    front_name: str
    state: str
    text: str
    language_short_name: str


@asyncinit
class HelpPublisher:
    HELP_URL = "http://repetitor_backend/api/v1/help/"

    async def __init__(self, kb_classes: list):
        self.help_messages_to_db = [
            {
                "front_name": "Telegram",
                "state": "NoTelegramState",
                "language_short_name": "en",
                "text": "You can enter any words according your language contexts for translation.",
            }
        ]

        # Перебираємо список класів Клавіатури та витягуємо з них параметри help_messages
        for kb_class in kb_classes:
            self.help_messages_to_db += kb_class.help_messages()

        # Отримуємо з БД UUID для мови за коротким ім'ям
        en_language = await get_context_by_short_name("en")
        self.languages_uuid = {"en": en_language[0]["id"]}

        for help_message in self.help_messages_to_db:
            if self.help_message_validator(help_message):
                print(f"HELP_VALIDATOR: Help for {help_message['state']} is correct!")
                # request_status = await self.__get_help_message_status(help_message)
                # if request_status == "404":
                #     if help_message["language_short_name"] not in self.languages_uuid.keys():
                #         any_language = await get_context_by_short_name(help_message["language_short_name"])
                #         self.languages_uuid = {"en": any_language[0]["id"]}
                #     help_message["language"] = self.languages_uuid[help_message["language_short_name"]]
                #     await self.__post_help_message(help_message)
        print(self.help_messages_to_db)

    async def __get_help_message_status(self, help_message) -> int:
        async with aiohttp.ClientSession() as session:
            params = help_message
            async with session.get(self.HELP_URL, params=params) as response:
                return response.status

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
