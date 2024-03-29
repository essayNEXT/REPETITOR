from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator

# from ..keyboard_translate.kb_translate import translate_context
from asyncinit import asyncinit
from utils.db.context import get_context
from aiogram import Dispatcher, Router
from typing import List
from utils.db.customer import update_user
from utils.help import HelpConstructor


@asyncinit
class ChooseNativeLanguageKeyboard(ContextInlineKeyboardGenerator, HelpConstructor):
    """Клавіатура вибору рідної мови користувача з доступних контекстів"""

    async def __init__(
        self,
        user_language: str,
        user_id: int = None,
        dp: Dispatcher | Router | None = None,
    ):
        self.__languages = await get_context()
        self.__languages = sorted(self.__languages, key=lambda x: x["name"])
        self.validation = [False]
        self.selected_data: List[str] | List[None] = [None]

        await super().__init__(user_language, user_id, dp)

    @property
    def initial_text(self) -> str:
        initial_text = "<b>Choose your native language from the list bellow.</b>"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "native_language_"
        return callback_pattern

    @property
    def max_rows_number(self) -> int:
        return 5

    @property
    def translate_function(self):
        # return translate_context
        return None

    @property
    def top_buttons(self) -> None:
        top_buttons = None
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        scroll_buttons = []
        for language in self.__languages:
            language_button = {
                "callback_data": self.callback_pattern
                + "lng_"
                + language["name_short"],
                "text": language["name"],
                "message": language["name"],
            }
            scroll_buttons.append([language_button])
        return scroll_buttons

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        bottom_buttons = [
            [
                {
                    "callback_data": "native_language_back",
                    "text": "Back 🔙",
                    "message": "Back 🔙",
                },
                {
                    "callback_data": "native_language_done",
                    "text": "Approve ☑️",
                    "message": "Native language selected ☑️",
                },
            ]
        ]
        return bottom_buttons

    @staticmethod
    def help_messages() -> list[dict]:
        help_message = [
            {
                "front_name": "Telegram",
                "state": "RegistrationForm:NATIVE_LANGUAGE_SELECTING",
                "language__name_short": "en",
                "text": "Use the '⬆️/⬇️' and '⏫️/⏬️' to scroll. The '⬆️/⬇️' scrolls one page at "
                "a time, the '⏬️' scrolls to the last page, the '⏫️' scrolls to the first "
                "page. Select your native language. After selecting press the 'APPROVE'.",
                "auto_translation": 1,
            }
        ]
        return help_message

    def language_selection_text(self):
        lng = self.messages[self.selected_data[0]]
        return self.text + f"\n[{lng}]"

    async def update_user_native_language(self):
        lng_short_name = self.selected_data[0].split("_")[-1]
        data = {"native_language": lng_short_name}
        await update_user(self.user_id, data)
