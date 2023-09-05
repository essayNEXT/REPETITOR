from abc import abstractmethod, ABC
from asyncinit import asyncinit
from typing_extensions import TypedDict
from pydantic import TypeAdapter, ValidationError
import aiohttp
from .db.context import get_context_by_short_name


class HelpMessageDict(TypedDict):
    front_name: str
    state: str
    text: str
    language__name_short: str
    auto_translation: int


class HelpConstructor(ABC):
    @staticmethod
    @abstractmethod
    def help_messages() -> list[HelpMessageDict]:
        pass


@asyncinit
class HelpPublisher:
    HELP_URL = "http://repetitor_backend/api/v1/help/"

    async def __init__(self, kb_classes: list):
        self.help_messages_to_db = [
            {
                "front_name": "Telegram",
                "state": "NoTelegramState",
                "language__name_short": "en",
                "text": "You can enter any words according to your language contexts for words translation.",
                "auto_translation": 1,
            },
            {
                "front_name": "Telegram",
                "state": "NoTelegramState",
                "language__name_short": "en",
                "text": "Now our feature is only word translation. Wait for another interesting possibilities.",
                "auto_translation": 1,
            },
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
                request_status = await self.__get_help_message_status(help_message)
                if request_status == 404:
                    if (
                        help_message["language__name_short"]
                        not in self.languages_uuid.keys()
                    ):
                        any_language = await get_context_by_short_name(
                            help_message["language__name_short"]
                        )
                        self.languages_uuid = {"en": any_language[0]["id"]}
                    help_message["language"] = self.languages_uuid[
                        help_message["language__name_short"]
                    ]
                    await self.__post_help_message(help_message)
                elif request_status in [200, 201]:
                    print(
                        f"HELP_PUBLISHER: Help for {help_message['state']} already is in database!"
                    )

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
            print(f"HELP_VALIDATOR: {err} - Wrong structure of help!")
            return False
