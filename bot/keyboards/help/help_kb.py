from aiogram import Dispatcher, Router

from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator

from asyncinit import asyncinit
import aiohttp


class HelpProblemKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура опису проблем з допомогою"""

    @property
    def initial_text(self) -> str:
        initial_text = "<b>What type of problem has occurred?</b>"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "help_problem_"
        return callback_pattern

    @property
    def max_rows_number(self) -> None:
        return None

    @property
    def translate_function(self):
        # return translate_context  # на етапі розробки поки не перекладатимемо клавіатури
        return None

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "help_problem_1",
                    "text": "Poor translation quality",
                    "message": "Poor translation quality",
                }
            ],
            [
                {
                    "callback_data": "help_problem_2",
                    "text": "Help does not match the problem",
                    "message": "Help does not match the problem",
                },
            ],
            [
                {
                    "callback_data": "help_problem_3",
                    "text": "The help does not fully answer the question",
                    "message": "The help does not fully answer the question",
                },
            ],
            [
                {
                    "callback_data": "help_problem_4",
                    "text": "There is a lot of extra information in the message",
                    "message": "There is a lot of extra information in the message",
                },
            ],
            [
                {
                    "callback_data": "help_problem_cancel",
                    "text": "❌",
                    "message": "Help problem report Cancel",
                },
            ],
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        return None

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        return None


@asyncinit
class HelpKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура допомоги користувачеві"""

    HELP_URL = "http://repetitor_backend/api/v1/help/"

    async def __init__(
        self,
        user_language: str,
        user_state: str | None,
        user_id: int = None,
        dp: Dispatcher | Router | None = None,
    ):
        self.user_state = user_state
        # Отримуємо дані з сервера на основі поточного стану
        if self.user_state is None:
            self.user_state = "NoTelegramState"

        self.data_from_backend = await self.__get_help_message(self.user_state, user_id)

        # Створюємо наступний рівень вкладеної клавіатури через змінну екземпляр клавіатури HelpProblemKeyboard
        self.problem_kb = await HelpProblemKeyboard(user_language, user_id, dp)

        # Створюємо сигнальні параметри відправлення позитивного та негативного відгуків для уникнення повторень
        self.positive_feedback = False
        self.negative_feedback = False

        await super().__init__(user_language, user_id, dp)

    @property
    def initial_text(self) -> str:
        initial_text = self.data_from_backend[0]["text"]
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "help_"
        return callback_pattern

    @property
    def max_rows_number(self) -> None:
        return None

    @property
    def translate_function(self):
        # return translate_context  # на етапі розробки поки не перекладатимемо клавіатури
        return None

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "help_thanks",
                    "text": "Thanks 👌",
                    "message": "We do our best for you ☺️",
                },
                {
                    "callback_data": "help_report_problem",
                    "text": "Report about problem 😡",
                    "message": "We will definitely make it better 🥲",
                },
            ],
            [
                {
                    "callback_data": "help_remove",
                    "text": "Remove help 🗑",
                    "message": "Remove help",
                },
            ],
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        return None

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        return None

    def problem_report_markup(self):
        return self.problem_kb.markup()

    @property
    def problem_report_text(self):
        return self.problem_kb.text

    async def __get_help_message(self, user_state, user_id) -> list | None:
        async with aiohttp.ClientSession() as session:
            params = {
                "state": user_state,
                "customer_tg_id": user_id,
                "front_name": "Telegram",
            }
            async with session.get(self.HELP_URL, params=params) as response:
                help_from_db = await response.json()
                return help_from_db

    async def __patch_help_message(
        self, params: dict, data_for_patch: dict
    ) -> list | None:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                self.HELP_URL, params=params, json=data_for_patch
            ) as response:
                help_from_db = await response.json()
                return help_from_db

    def positive_message(self) -> str:
        return self.messages["help_thanks"]

    def negative_message(self) -> str:
        return self.messages["help_report_problem"]

    async def send_positive_feedback(self):
        if not self.positive_feedback:
            params = {"id": self.data_from_backend[0]["id"]}
            data_for_patch = {
                "modifying_positive_feedback": 1,
            }
            await self.__patch_help_message(params, data_for_patch)
            self.positive_feedback = True

    async def send_negative_feedback(self):
        if not self.negative_feedback:
            params = {"id": self.data_from_backend[0]["id"]}
            data_for_patch = {
                "modifying_negative_feedback": 1,
            }
            await self.__patch_help_message(params, data_for_patch)
            self.negative_feedback = True

    async def send_problem_report(self, problem: str):
        # TO DO в майбутньому має з'явитись можливість надсилати опис проблему
        print(
            f"HELP_PROBLEM_REPORT: user {self.user_id} for  help state [{self.user_state}] report '{problem}'"
        )
