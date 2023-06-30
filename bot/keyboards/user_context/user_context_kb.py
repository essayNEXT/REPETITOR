from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator
from ..keyboard_translate.kb_translate import translate_context

# from utils.db.context import get_context


class ChooseContextKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура визначення контексту користувача"""

    @property
    def selected_data(self) -> list:
        selected_data = [None, None]
        return selected_data

    @property
    def initial_text(self) -> str:
        initial_text = "<b>Оберіть базову та цільову мови.</b>"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "uk"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "create_user_context"
        return callback_pattern

    @property
    def max_rows_number(self) -> int:
        return 3

    @property
    def translate_function(self):
        return translate_context

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "create_user_context_1",
                    "text": "Базова мова",
                    "message": "Базова мова",
                }
            ],
            [
                {
                    "callback_data": "create_user_context_2",
                    "text": "Цільова мова",
                    "message": "Цільова мова",
                }
            ],
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        return None

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        bottom_buttons = [
            [
                {
                    "callback_data": "create_user_context_done",
                    "text": "Підтвердити",
                    "message": "Контекст користувача створено!",
                }
            ]
        ]
        return bottom_buttons
