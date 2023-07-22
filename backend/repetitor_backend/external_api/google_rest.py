import os
from dotenv import load_dotenv
from aiohttp import ClientSession


load_dotenv()
URL = "https://translation.googleapis.com/language/translate/v2"
API_KEY = os.environ.get("GOOGLE_API_KEY")


async def translate(
    session: ClientSession = None,
    source_lng: str = "en",
    target_lng: str = "uk",
    text: str = "add",
    url: str = URL,
    api_key: str = API_KEY,
) -> tuple:
    """
    The function performs automatic translation of a word in a given context from two languages,
    the order of languages does not matter
    Google Translate REST API is used

    :param session: aiohttp.ClientSession
    :param source_lng: first language
    :param target_lng: second language
    :param text: text to be translated
    :param url: address to request a text translation
    :param api_key: access key
    :return: tuple(result, target language) - if the translation is correct,
             else tuple ('Translation ERROR',)
    """
    from repetitor_backend.app import app

    if not session:
        session = app.session

    text = text.lower()
    params = {"q": text, "source": source_lng, "target": target_lng, "key": api_key}

    params_reverse = {
        "q": text,
        "source": target_lng,
        "target": source_lng,
        "key": api_key,
    }

    async with session.post(url, data=params) as response:
        translation = await response.json()
        translated_text = translation["data"]["translations"][0][
            "translatedText"
        ].lower()

    async with session.post(url, data=params_reverse) as response_reverse:
        translation_reverse = await response_reverse.json()
        translated_reverse = translation_reverse["data"]["translations"][0][
            "translatedText"
        ].lower()

    # print('translated_text:', translated_text)
    # print('translated_reverse:', translated_reverse)

    res = (
        [translated_reverse, source_lng, target_lng]
        if text == translated_text
        else [translated_text, target_lng, source_lng]
    )

    # перевірка результату
    txt, src_lng, trg_lng = res

    params_verification = {
        "q": txt,
        "source": src_lng,
        "target": trg_lng,
        "key": api_key,
    }

    async with session.post(url, data=params_verification) as response_verification:
        translation_verification = await response_verification.json()
        translated_verification = translation_verification["data"]["translations"][0][
            "translatedText"
        ].lower()
    # print('translated_verification', translated_verification)

    return tuple(res[:2]) if text == translated_verification else ("Translation ERROR",)
