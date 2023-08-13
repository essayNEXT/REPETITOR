import os
import uuid
from dotenv import load_dotenv
from aiohttp import ClientSession
from .accents import remove_accents


load_dotenv()
URL = "https://api.cognitive.microsofttranslator.com/translate"
URL_lNG = "https://api.cognitive.microsofttranslator.com/languages"
API_KEY = os.environ.get("KEY_MICROSOFT")
LOCATION = os.environ.get("LOCATION")
MICROSOFT_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")


async def translate(
    session: ClientSession = None,
    source_lng: str = "en",
    target_lng: str = "uk",
    text: str = "add",
    url: str = URL,
    api_key: str = API_KEY,
    location: str = LOCATION,
) -> tuple:
    """
    The function performs automatic translation of the word in the specified context
    of the languages, the order of the languages does not matter
    Used Microsoft Azure Cognitive Services Translator REST APIs

    :param session: aiohttp.ClientSession
    :param source_lng: first language
    :param target_lng: second language
    :param text: text to be translated
    :param url: address to request a text translation
    :param api_key: access key
    :param location: site location for the request
    :return: tuple(result, target language, MICROSOFT_UUID) - if the translation is correct,
             else tuple ('Translation ERROR',)
    """

    # from repetitor_backend.app import app
    #
    # if not session:
    #     session = app.session

    text = remove_accents(text.lower())

    params = {"api-version": "3.0", "to": [target_lng]}  # "from": source_lng,
    params_reverse = {"api-version": "3.0", "to": [source_lng]}  # "from": target_lng,

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
    }
    # import uuid
    # "X-ClientTraceId": str(uuid.uuid4()), - A client-generated GUID to uniquely identify the request.

    # You can pass more than one object in body.
    body = [{"text": text}]

    async with session.post(url, params=params, headers=headers, json=body) as response:
        response_data = await response.json()
        translated = remove_accents(response_data[0]["translations"][0]["text"].lower())
        detected_src_lng = response_data[0]["detectedLanguage"]["language"]

    # print()
    # print('MS translate')
    # print(f"text_to_translate: {text}, src_lng: {source_lng}, detected_src_lng: {detected_src_lng}")
    # print(f"translated_text: {translated}, target_lng: {target_lng}")

    if source_lng == detected_src_lng and text != translated:  # qwerty
        return translated, target_lng, MICROSOFT_UUID

    elif target_lng == detected_src_lng and text != translated:
        async with session.post(
            url, params=params_reverse, headers=headers, json=body
        ) as response:
            response_data = await response.json()

            translated_reverse = remove_accents(
                response_data[0]["translations"][0]["text"].lower()
            )
        return translated_reverse, source_lng, MICROSOFT_UUID
    else:
        return ("Translation ERROR",)


async def translate_lng(
    session: ClientSession = None,
    interface_lng: str = "en",
    url: str = URL_lNG,
) -> dict:
    """
    Gets the set of languages currently supported by other operations of the Translator.
    https://learn.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-languages#response-body
    Args:
        session: aiohttp.ClientSession
        interface_lng: full names of languages are displayed in the interface language
        url: address for requesting languages supported by the translation

    Returns: Dict of supported languages
    response_data["translation"] = {
    'af': {'name': 'Afrikaans', 'nativeName': 'Afrikaans', 'dir': 'ltr'},
    'am': {'name': 'Amharic', 'nativeName': 'አማርኛ', 'dir': 'ltr'}...}

    lang_dict = {'af': 'Afrikaans', 'am': 'Amharic', ...}
    """

    if session is None:
        from repetitor_backend.app import app

        session = app.session

    params = {
        "api-version": "3.0",
        "scope": "translation",
    }  # scope = translation,transliteration,dictionary

    headers = {
        "Accept-Language": interface_lng,
    }

    async with session.get(url, params=params, headers=headers) as response:
        response_data = await response.json()

    lang_dict_full = response_data["translation"]
    lang_dict = {key: value["name"] for key, value in lang_dict_full.items()}

    return lang_dict
