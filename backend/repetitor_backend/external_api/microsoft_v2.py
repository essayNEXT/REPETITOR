import aiohttp
import asyncio
import os
from dotenv import load_dotenv
import time


load_dotenv()
URL = "https://api.cognitive.microsofttranslator.com/translate"
URL_lNG = "https://api.cognitive.microsofttranslator.com/languages"
# https://api-eur.cognitive.microsofttranslator.com Північна Європа, Західна Європа
API_KEY = os.environ.get("KEY_MICROSOFT")
LOCATION = os.environ.get("LOCATION")

# session = aiohttp.ClientSession()
# async def main():
#     async with session.get('http://httpbin.org/get') as resp:
#         print(resp.status)
    # print(await resp.text())

# asyncio.run(main())
# await session.close()

async def translate(
    session,
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

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
    }

    # You can pass more than one object in body.
    body = [{"text": text}]

    # async with aiohttp.ClientSession() as session:
    async with session.post(
        url, params=params, headers=headers, json=body
    ) as response:
        response_data = await response.json()
        response_data = source_lng, response_data[0]["translations"][0]["text"]
        # print(response_data)
        res = response_data[1]
        # return res

    # We perform a reverse translation
    time.sleep(1)
    body_rev = [{"text": res}]
    async with session.post(
        url, params=params_reverse, headers=headers, json=body_rev
    ) as response:
        response_data = await response.json()
        response_data = source_lng, response_data[0]["translations"][0]["text"]
        res_rev = response_data[1]
        # print(text.lower(), res_rev.lower())

    return res if text.lower() == res_rev.lower() else "Translation error"


# async def main(source_lng, target_lng, text):
#     async with aiohttp.ClientSession() as session:
#         res = await translate(session, source_lng, target_lng, text)
#         return res

