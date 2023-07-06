from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator

# from ..keyboard_translate.kb_translate import translate_context
from asyncinit import asyncinit
from utils.db.context import get_context, get_context_by_short_name
from utils.db.customer import get_user
from utils.db.customer_context import create_customer_context
from aiogram import Dispatcher, Router
from typing import List


@asyncinit
class ChooseContextKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура створення контексту користувача"""

    async def __init__(
        self,
        user_language: str,
        user_id: int = None,
        dp: Dispatcher | Router | None = None,
    ):
        self.__contexts = await get_context()
        self.__contexts = sorted(self.__contexts, key=lambda x: x["name"])
        self.validation = [False, False]
        self.selected_data: List[str] | List[None] = [None, None]

        await super().__init__(user_language, user_id, dp)

    @property
    def initial_text(self) -> str:
        initial_text = "<b>Choose BASE and TARGET languages.</b>"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "create_user_context_"
        return callback_pattern

    @property
    def max_rows_number(self) -> int:
        return 5

    @property
    def translate_function(self):
        # return translate_context
        return None

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "create_user_context_con_1",
                    "text": "BASE",
                    "message": "Choose Base language ⬇️",
                },
                {
                    "callback_data": "create_user_context_con_2",
                    "text": "TARGET",
                    "message": "Choose Target language ⬇️",
                },
            ],
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        scroll_buttons = []
        for context in self.__contexts:
            language = {
                "callback_data": self.callback_pattern + "lng_" + context["name_short"],
                "text": context["name"],
                "message": context["name"],
            }
            scroll_buttons.append([language])
        return scroll_buttons

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        bottom_buttons = [
            [
                {
                    "callback_data": "create_user_context_done",
                    "text": "APPROVE ☑️",
                    "message": "Context created ☑️",
                }
            ]
        ]
        return bottom_buttons

    def context_selection_text(self):
        con_1 = self.messages[self.selected_data[0]] if self.selected_data[0] else "???"
        con_2 = self.messages[self.selected_data[1]] if self.selected_data[1] else "???"
        return f"[{con_1}] >>> [{con_2}]"

    async def create_customer_context(self):
        user_data = await get_user(self.user_id)
        user_uuid = user_data[0]["id"]

        context_1_data = await get_context_by_short_name(
            self.selected_data[0].split("_")[-1]
        )
        context_1_uuid = context_1_data[0]["id"]

        context_2_data = await get_context_by_short_name(
            self.selected_data[1].split("_")[-1]
        )
        context_2_uuid = context_2_data[0]["id"]

        result = await create_customer_context(
            user_uuid, context_1_uuid, context_2_uuid
        )
        print("New customer_context id:", result)
