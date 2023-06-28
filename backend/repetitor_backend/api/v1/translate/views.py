import logging
from repetitor_backend.external_api.microsoft import translate, translate_lng
from fastapi import APIRouter

logger = logging.getLogger()

router = APIRouter()


@router.get("/translate/ms_lng_list/")
async def ms_lng_list(int_lng: str = "en") -> list:
    """Отримує список мов, які зараз підтримуються операціями Перекладача."""
    from repetitor_backend.app import app

    result = await translate_lng(session=app.session, interface_lng=int_lng)
    return list(result)


@router.get("/translate/ms_translate/")
async def ms_translate(
    src_lng: str = "uk", trg_lng: str = "en", text: str = "додати"
) -> str:
    """
    The function returns the translation of the entered text, in addition,
    it compares the resulting translation with:
    1. by reverse translation or
    2. with the translation "auto-detecting input language"
        (additional option, not used yet)
       and decides on the correctness of the translation.
    Used Microsoft Azure Cognitive Services Translator REST APIs

    :param source_lang: language from which the translation is carried out
    :param target_lang: language into which the translation is carried out
    :param text: text to be translated
    :return: if the translation is correct, then returns the translation of the input text
    """

    from repetitor_backend.app import app

    result = await translate(app.session, src_lng, trg_lng, text)
    return result
