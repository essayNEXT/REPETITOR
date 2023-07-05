import os
from dotenv import load_dotenv
import time
# from aiohttp import ClientSession
# from repetitor_backend.app import app

load_dotenv()
URL = "https://api.cognitive.microsofttranslator.com/translate"
URL_lNG = "https://api.cognitive.microsofttranslator.com/languages"
API_KEY = os.environ.get("KEY_MICROSOFT")
LOCATION = os.environ.get("LOCATION")


async def translate(
    session,
    source_lng: str = 'en',
    target_lng: str = 'uk',
    text: str = 'add',
    url: str = URL,
    api_key: str = API_KEY,
    location: str = LOCATION,
) -> str:
    """
    The function returns the translation of the entered text, in addition,
    it compares the resulting translation with:
    1. by reverse translation or
    2. with the translation "auto-detecting input language"
        (additional option, not used yet)
       and decides on the correctness of the translation.
    Used Microsoft Azure Cognitive Services Translator REST APIs

    :param session: aiohttp.ClientSession
    :param source_lng: language from which the translation is carried out
    :param target_lng: language into which the translation is carried out
    :param text: text to be translated
    :param url: address to request a text translation
    :param api_key: access key
    :param location: site location for the request
    :return: if the translation is correct, then returns the translation of the input text
    """

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
    body = [{"text": text.lower()}]
    print('text = ', text.lower())
    async with session.post(url, params=params, headers=headers, json=body) as response:
        response_data = await response.json()
        response_data = source_lng, response_data[0]["translations"][0]["text"]
        res = response_data[1]
        print('res = ', res)

    async with session.post(url, params=params_reverse, headers=headers, json=body) as response:
        response_data = await response.json()
        response_data = source_lng, response_data[0]["translations"][0]["text"]
        res_rev2 = response_data[1]
        print('res_rev2 = ', res_rev2)

    # We perform a reverse translation
    time.sleep(1)
    body_rev = [{"text": res}]
    async with session.post(
        url, params=params_reverse, headers=headers, json=body_rev
    ) as response:
        response_data = await response.json()
        response_data = source_lng, response_data[0]["translations"][0]["text"]
        res_rev = response_data[1]
        print('res_rev = ', res_rev)

    if res_rev2.lower() != text:
        async with session.post(url, params=params, headers=headers, json=body) as response:
            response_data = await response.json()
            response_data = source_lng, response_data[0]["translations"][0]["text"]
            res2 = response_data[1]
            print('res2 = ', res2)

    return res if text.lower() == res_rev.lower() else res_rev2


async def translate_lng(
    session,
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
