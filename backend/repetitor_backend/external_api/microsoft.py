import aiohttp
import asyncio
import uuid
import os
from dotenv import load_dotenv


load_dotenv()
URL = "https://api.cognitive.microsofttranslator.com/translate"
API_KEY = os.environ.get("KEY_MICROSOFT")
LOCATION = os.environ.get("LOCATION")

# session = aiohttp.ClientSession() - помилка, цей параметр треба задавати в асинхроній функції


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
    it compares the received translation with the "auto-detect input language"
    translation and decides on the correctness of the translation.
    Used Microsoft Azure Cognitive Services Translator REST APIs
    :param source_lang: language from which the translation is carried out
    :param target_lang: language into which the translation is carried out
    :param text: text to be translated
    :return: if the translation is correct, then returns the translation of the input text
    """

    params = {"api-version": "3.0", "from": source_lng, "to": [target_lng]}

    # autodetect source language
    params_auto = {"api-version": "3.0", "to": [target_lng]}

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    # You can pass more than one object in body.
    body = [{"text": text}]

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, params=params, headers=headers, json=body
        ) as response:
            response_data = await response.json()
            response_data = source_lng, response_data[0]["translations"][0]["text"]
            print(response_data)

        async with session.post(
            url, params=params_auto, headers=headers, json=body
        ) as response:
            response_data_auto = await response.json()
            response_data_auto = (
                response_data_auto[0]["detectedLanguage"]["language"],
                response_data_auto[0]["translations"][0]["text"],
            )
            print(response_data_auto)
            if response_data == response_data_auto:
                print("The translation is correct")
                return response_data[1]
            else:
                print("Translation error")
                return "Translation error"


if __name__ == "__main__":
    source_lng = "en"
    target_lng = "uk"
    text = "dog"

    # bg("куче") = en("dog") - провокуєм помилку
    # source_lng = "uk"
    # target_lng = "en"
    # text = "куче"

    loop = asyncio.get_event_loop()
    loop.run_until_complete(translate(source_lng, target_lng, text))
