from aiogram import Dispatcher, Router

from ..inline_keyboard import KeyboardOfDict, ContextInlineKeyboardGenerator

# from ..keyboard_translate.kb_translate import translate_context
from asyncinit import asyncinit
from utils.db.translate_text import get_translate_text


@asyncinit
class TextTranslateKeyboard(ContextInlineKeyboardGenerator):
    """Клавіатура перекладу слів"""

    async def __init__(
        self,
        user_language: str,
        text_for_translate: str,
        user_id: int = None,
        dp: Dispatcher | Router | None = None,
    ):
        self.text_for_translate = text_for_translate
        self.data_from_backend = await get_translate_text(text_for_translate, user_id)

        await super().__init__(user_language, user_id, dp)

    @property
    def initial_text(self) -> str:
        initial_text = "<b>This is translate of your word {} - {} </b>"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "text_translate_"
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
                    "callback_data": "text_translate_ok",
                    "text": "Ok",
                    "message": "Ok",
                },
                {
                    "callback_data": "text_translate_my_translation",
                    "text": "My translation",
                    "message": "Enter your translation for word {} :",
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

    def massage_for_translation_text(self):
        translated_text = self.data_from_backend[0]["item_text_2"]
        result = self.text.format(self.text_for_translate, translated_text)
        return result

    def message_for_user_translation(self):
        return self.messages["text_translate_my_translation"].format(
            self.text_for_translate
        )

    def add_user_translation(self, user_translation):
        print(f"adding user translation {self.text_for_translate} - {user_translation}")
        pass
