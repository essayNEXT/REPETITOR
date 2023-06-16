import aiohttp
import os
from dotenv import load_dotenv
import time


load_dotenv()
URL = "https://api.cognitive.microsofttranslator.com/translate"
URL_lNG = "https://api.cognitive.microsofttranslator.com/languages"
# https://api-eur.cognitive.microsofttranslator.com Північна Європа, Західна Європа
API_KEY = os.environ.get("KEY_MICROSOFT")
LOCATION = os.environ.get("LOCATION")


async def translate(
    source_lng: str,
    target_lng: str,
    text: str,
    url: str = URL,
    api_key: str = API_KEY,
    location: str = LOCATION,
) -> aiohttp.ClientResponse:
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

    params = {"api-version": "3.0", "from": source_lng, "to": [target_lng]}
    params_reverse = {"api-version": "3.0", "from": target_lng, "to": [source_lng]}

    # autodetect source language
    # params_auto = {"api-version": "3.0", "to": [target_lng]}

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
    }
    # import uuid
    # "X-ClientTraceId": str(uuid.uuid4()), - A client-generated GUID to uniquely identify the request.

    # You can pass more than one object in body.
    body = [{"text": text}]


    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, params=params, headers=headers, json=body
        ) as response:
            response_data = await response.json()
            response_data = source_lng, response_data[0]["translations"][0]["text"]
            # print(response_data)
            res = response_data[1]

        # 1. We perform a reverse translation
        time.sleep(1)
        body_rev = [{"text": res}]
        async with session.post(
                url, params=params_reverse, headers=headers, json=body_rev
        ) as response:
            response_data = await response.json()
            response_data = source_lng, response_data[0]["translations"][0]["text"]
            res_rev = response_data[1]
            #print(text.lower(), res_rev.lower())

        return res if text.lower() == res_rev.lower() else "Translation error"

        # 2. Translation with the "auto-detect input language"
        # async with session.post(
        #     url, params=params_auto, headers=headers, json=body
        # ) as response:
        #     response_data_auto = await response.json()
        #     response_data_auto = (
        #         response_data_auto[0]["detectedLanguage"]["language"],
        #         response_data_auto[0]["translations"][0]["text"],
        #     )
        #     print(response_data_auto)
        #     if response_data == response_data_auto:
        #         #print("The translation is correct")
        #         return response_data[1]
        #     else:
        #         # res = response_data[1]
        #         # source_lng, target_lng = target_lng, source_lng
        #         print("Translation error")

async def translate_lng(
    interface_lng: str,   # accept_language
    url: str = URL_lNG,
) -> aiohttp.ClientResponse:
    """ Отримує набір мов, які зараз підтримуються іншими операціями Перекладача. """

    params = {"api-version": "3.0", "scope": "translation"}  # translation,transliteration,dictionary}

    headers = {"Accept-Language": interface_lng, }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, params=params, headers=headers
        ) as response:
            response_data = await response.json()

        return response_data["translation"]
