from deep_translator import GoogleTranslator
from typing import TypeVar

ButtonDictList = TypeVar("ButtonDictList")

# Імітація бази даних перекладу клавіатури
translation = {"uk": {}, "en": {}, "ru": {}}

# Імітація бази даних одиничних перекладів рядків
single_translation = {"uk": {}, "en": {}, "ru": {}}


def google_translate(src_lng: str, trg_lng: str, input_text: str) -> str:
    """Функція перекладу тексту за допомогою перекладача гугл.
    Приймає:
        - src_lng: str - мова об'єкту, що перекладається
        - trg_lng: str - цільова мова перекладу
        - input_text: str - текст для перекладу
    Повертає рядок з перекладеним текстом"""
    tr = GoogleTranslator(source=src_lng, target=trg_lng).translate(input_text)
    return tr


def translate_buttons_list(
    source_lng: str, target_lng: str, buttons_list: ButtonDictList
) -> ButtonDictList:
    """Функція перекладу списку списків словників кнопок клавіатури"""

    if buttons_list is None:
        return []
    new_list = []
    for item in buttons_list:
        if isinstance(item, list):
            new_list.append(translate_buttons_list(source_lng, target_lng, item))
        elif isinstance(item, dict):
            item["text"] = google_translate(
                source_lng, target_lng, item["text"]
            ).capitalize()
            if "message" in item.keys():
                item["message"] = google_translate(
                    source_lng, target_lng, item["message"]
                )
            new_list.append(item)
    return new_list


def translate_text(src_lng, trg_lng, context_text) -> str:
    """
    Переклад тексту:
        - src_lng: str - мова об'єкту, що перекладається
        - trg_lng: str - цільова мова перекладу
        - context_text: str - текст, що необхідно перекласти
    """

    if src_lng == trg_lng:
        print(f"TRANSLATOR: {context_text} - is in keyboard object")
        return context_text
    else:
        if (
            trg_lng in single_translation.keys()
            and context_text in single_translation[trg_lng].keys()
        ):
            print(f"TRANSLATOR: {context_text} - is get from db")
            return single_translation[trg_lng][context_text]
        else:
            print(f"TRANSLATOR: {context_text} - is get from Google translate")
            text = google_translate(src_lng, trg_lng, context_text)

            # імітація занесення перекладу до БД single_translation
            if trg_lng not in single_translation.keys():
                single_translation[trg_lng] = {}
            single_translation[trg_lng][context_text] = text
            return text


def translate_kb_dict(self_object, context_data) -> dict:
    """
    Переклад контекстних даних екземпляру клавіатури:
        - self_object - екземпляр класу клавіатури
        - context_data: dict - словник з даними для перекладу, що містить в собі:
            "initial_text" - початковий текст при виклику клавіатури
            "top_buttons" - список списків верхніх кнопок
            "scroll_buttons" - список списків кнопок прокручування
            "bottom_buttons" - список списків нижніх кнопок
    """
    src_lng = self_object.kb_language
    trg_lng = self_object.user_language

    if src_lng == trg_lng:
        print("TRANSLATOR: Don`t need to translate!")
        return context_data

    # Перевіряємо наявність перекладу context_data для класу клавіатури в базі даних
    if (
        trg_lng in translation.keys()
        and str(self_object.__class__) in translation[trg_lng].keys()
    ):
        print("TRANSLATOR: Context_data - get from db!")
        return translation[trg_lng][str(self_object.__class__)]  # повинні отримати з БД
    # Якщо в базі даних переклад відсутній, то виконуємо переклад поелементно
    else:
        print(
            f"TRANSLATOR: Google translate every single element of context_data from {src_lng} to {trg_lng}!"
        )
        context_data["initial_text"] = google_translate(
            src_lng, trg_lng, context_data["initial_text"]
        )
        context_data["top_buttons"] = translate_buttons_list(
            src_lng, trg_lng, context_data["top_buttons"]
        )
        context_data["scroll_buttons"] = translate_buttons_list(
            src_lng, trg_lng, context_data["scroll_buttons"]
        )
        context_data["bottom_buttons"] = translate_buttons_list(
            src_lng, trg_lng, context_data["bottom_buttons"]
        )

        # імітуємо занесення перекладу клавіатур на мову користувача дл бази даних
        if trg_lng not in translation.keys():
            translation[trg_lng] = {}
        translation[trg_lng][str(self_object.__class__)] = context_data

        return context_data


def translate_context(
    src_lng: str = None,
    trg_lng: str = None,
    context_text: str = None,
    self_object=None,
    context_data: dict = None,
):
    """
    Функція перекладу контексту. Приймає два варіанти вхідних даних:
    1. Переклад тексту:
        - src_lng: str - мова об'єкту, що перекладається
        - trg_lng: str - цільова мова перекладу
        - context_text: str - текст, що необхідно перекласти
    2. Переклад контекстних даних екземпляру клавіатури:
        - self_object - екземпляр класу клавіатури
        - context_data: dict - словник з даними для перекладу, що містить в собі:
            "initial_text" - початковий текст при виклику клавіатури
            "top_buttons" - список списків верхніх кнопок
            "scroll_buttons" - список списків кнопок прокручування
            "bottom_buttons" - список списків нижніх кнопок
    Повертає відповідні об'єкти в залежності від варіанту введених вхідних даних.
    """

    try:
        if context_text and context_data:
            raise KeyError("Input data is not correct!")

        # Варіант 1
        elif context_text:
            return translate_text(src_lng, trg_lng, context_text)

        # Варіант 2
        elif self_object and context_data:
            return translate_kb_dict(self_object, context_data)
        else:
            return None
    except KeyError as e:
        print(f"TRANSLATOR: Error {e}")
