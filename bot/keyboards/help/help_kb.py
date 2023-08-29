from aiogram import Dispatcher, Router

from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator

from asyncinit import asyncinit


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
                    "text": "Problem #1",
                    "message": "Problem #1",
                }
            ],
            [
                {
                    "callback_data": "help_problem_2",
                    "text": "Problem #2",
                    "message": "Problem #2",
                },
            ],
            [
                {
                    "callback_data": "help_problem_3",
                    "text": "Problem #3",
                    "message": "Problem #3",
                },
            ],
            [
                {
                    "callback_data": "help_problem_4",
                    "text": "Problem #4",
                    "message": "Problem #4",
                },
            ],
            [
                {
                    "callback_data": "help_problem_4",
                    "text": "Problem #4",
                    "message": "Problem #4",
                },
            ],
            [
                {
                    "callback_data": "help_problem_cancel",
                    "text": "❌",
                    "message": "Cancel",
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
            self.user_state = "No_Telegram_state"
        self.data_from_backend = [
            {
                "state_name": "No_Telegram_state",
                "language_code": "en",
                "help_text": "Do anything you want now. Here some of commands and possibilities: ...",
            }
        ]

        # Створюємо наступний рівень вкладеної клавіатури через змінну екземпляр клавіатури HelpProblemKeyboard
        self.problem_kb = HelpProblemKeyboard(user_language, user_id, dp)

        await super().__init__(user_language, user_id, dp)

    @property
    def initial_text(self) -> str:
        initial_text = self.data_from_backend[0]["help_text"]
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
                    "callback_data": "help_ok",
                    "text": "Ok",
                    "message": "Ok",
                },
                {
                    "callback_data": "help_report_problem",
                    "text": "Report about problem",
                    "message": "Report about problem",
                },
            ]
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
