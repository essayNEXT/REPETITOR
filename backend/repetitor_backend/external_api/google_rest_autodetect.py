import os
from dotenv import load_dotenv
from aiohttp import ClientSession
from .accents import remove_accents


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
    :return: tuple(result, target language, GOOGLE_UUID) - if the translation is correct,
             else tuple ('Translation ERROR',)
    """
    from repetitor_backend.app import app

    if not session:
        session = app.session

    text = remove_accents(text.lower())
    params = {"q": text, "target": target_lng, "key": api_key}

    async with session.post(url, data=params) as response:
        translation = await response.json()
        translated_text = remove_accents(
            translation["data"]["translations"][0]["translatedText"].lower()
        )
        detected_src_lng = translation["data"]["translations"][0]["detectedSourceLanguage"]

    print()
    print("GOOGLE translate")
    print(f"text_to_translate: {text}, src_lng: {source_lng}, detected_src_lng: {detected_src_lng}")
    print(f"translated_text: {translated_text}, target_lng: {target_lng}")

    if source_lng == detected_src_lng:
        return translated_text, target_lng, "00000000-0000-0000-0000-000000000001"

    elif target_lng == detected_src_lng:  # text == translated_text and
        params = {"q": text, "target": source_lng, "key": api_key}
        async with session.post(url, data=params) as response:
            translation = await response.json()
            translated_text = remove_accents(
                translation["data"]["translations"][0]["translatedText"].lower()
            )

        return translated_text, source_lng, "00000000-0000-0000-0000-000000000001"
    else:
        return ("Translation ERROR",)
