from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator
from ..keyboard_translate.kb_translate import translate_context


class RegisterKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура реєстрації"""

    @property
    def initial_text(self) -> str:
        initial_text = "Hello, {}!\nYou need to registrate for using my functions."
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "registration"
        return callback_pattern

    @property
    def max_rows_number(self) -> None:
        return None

    @property
    def translate_function(self):
        return translate_context

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {
                    "callback_data": "registration",
                    "text": "Register",
                    "message": "Register",
                }
            ]
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict | None:
        return None

    @property
    def bottom_buttons(self) -> KeyboardOfDict | None:
        return None
