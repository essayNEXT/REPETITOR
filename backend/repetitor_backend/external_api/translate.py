from aiohttp import ClientSession
from .google_rest_autodetect import translate as gg_auto
from .google_rest import translate as gg_fix
from .microsoft import translate as ms_auto


async def translate(
    session: ClientSession = None,
    source_lng: str = "en",
    target_lng: str = "uk",
    text: str = "add",
) -> tuple:
    """
    The function performs automatic translation of a word in a given context from two languages,
    the order of languages does not matter
    1. Used Microsoft Azure Cognitive Services Translator REST APIs
    2. Google Translate REST API is used autodect language
    3. Google Translate REST API is used fix language

    :param session: aiohttp.ClientSession
    :param source_lng: first language
    :param target_lng: second language
    :param text: text to be translated

    :return: 1.tuple(result, target language, MICROSOFT_UUID) - if the translation is correct,
             else tuple ('Translation ERROR',)
             2.tuple(result, target language, GOOGLE_UUID) - if the translation is correct,
             else tuple ('Translation ERROR',)
            3.tuple(result, target language, GOOGLE_UUID, True) - if the translation + verification is correct,
            else tuple (result, target language, GOOGLE_UUID, False) if verification is incorrect

    """

    from repetitor_backend.app import app

    if not session:
        session = app.session

    # GOOGLE translate
    try:
        result = await gg_auto(
            session, text=text, source_lng=source_lng, target_lng=target_lng
        )
        print("result GG = ", result)
    except Exception:
        print("Google_auto ERROR")
        result = ("Google_auto ERROR",)

    # MS translate
    if len(result) == 1:
        try:
            result = await ms_auto(
                session, text=text, source_lng=source_lng, target_lng=target_lng
            )
            print("result MS = ", result)
        except Exception:
            print("MS ERROR")
            result = ("Google_auto ERROR & MS ERROR",)

        # GOOGLE fix translate
        if len(result) == 1:
            try:
                result = await gg_fix(
                    session, text=text, source_lng=source_lng, target_lng=target_lng
                )
                print("result fix = ", result)
            except Exception:
                print("Google_fix ERROR")
                result = ("Google_auto ERROR & MS ERROR & Google_fix ERROR",)
    return result
