import os
from dotenv import load_dotenv
from aiohttp import ClientSession

# from repetitor_backend.app import app


load_dotenv()
URL = "https://api.cognitive.microsofttranslator.com/translate"
URL_lNG = "https://api.cognitive.microsofttranslator.com/languages"
API_KEY = os.environ.get("KEY_MICROSOFT")
LOCATION = os.environ.get("LOCATION")


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
    :return: tuple(result, target language) - if the translation is correct,
             then returns the translation of the input text
    """
    from repetitor_backend.app import app

    if not session:
        session = app.session

    text = text.lower()
    params = {"api-version": "3.0", "from": source_lng, "to": [target_lng]}
    params_reverse = {"api-version": "3.0", "from": target_lng, "to": [source_lng]}

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
        translated = response_data[0]["translations"][0]["text"].lower()

    async with session.post(
        url, params=params_reverse, headers=headers, json=body
    ) as response:
        response_data = await response.json()
        translated_reverse = response_data[0]["translations"][0]["text"].lower()

    res = (
        [translated_reverse, source_lng, target_lng]
        if text == translated
        else [translated, target_lng, source_lng]
    )

    # print('translated_text:', translated)
    # print('translated_reverse:', translated_reverse)

    # перевірка результату
    txt, src_lng, trg_lng = res

    body_verif = [{"text": txt}]
    params_verif = {"api-version": "3.0", "from": src_lng, "to": [trg_lng]}

    async with session.post(
        url, params=params_verif, headers=headers, json=body_verif
    ) as response_verif:
        translation_verif = await response_verif.json()
        translated_verif = translation_verif[0]["translations"][0]["text"].lower()
    # print('translated_verification', translated_verif)

    return tuple(res[:2]) if text == translated_verif else ("Translation ERROR",)


async def translate_lng(
    session: ClientSession,
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
    """

    params = {
        "api-version": "3.0",
        "scope": "translation",
    }  # scope = translation,transliteration,dictionary

    headers = {
        "Accept-Language": interface_lng,
    }

    async with session.get(url, params=params, headers=headers) as response:
        response_data = await response.json()

    return response_data["translation"]
