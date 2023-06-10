import requests
import uuid
import os
from dotenv import load_dotenv


load_dotenv()


def ms_translate(source_lang: str, target_lang: str, text: str) -> str:
    """
    The function returns the translation of the entered text, used
    Microsoft Azure Cognitive Services Translator REST APIs
    :param source_lang: language from which the translation is carried out
    :param target_lang: language into which the translation is carried out
    :param text: text to be translated
    :return: translated text
    """

    # Add your key and endpoint
    key = os.environ.get("KEY_MICROSOFT")
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # location, also known as region.
    # required if you"re using a multi-service or regional (not global) resource.
    # It can be found in the Azure portal on the Keys and Endpoint page.
    location = os.environ.get("LOCATION")

    path = "/translate"
    constructed_url = endpoint + path

    params = {"api-version": "3.0", "from": source_lang, "to": [target_lang]}

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        # location required if you"re using a multi-service or regional (not global) resource.
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    # You can pass more than one object in body.
    body = [{"text": text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    # import json
    # json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(",", ": "))

    translate = response[0]["translations"][0]["text"]
    return translate

def ms_translate_auto(target_lang: str, text: str) -> str:
    """
    The function returns the translation of the entered text with autodetect source_lang,
    used Microsoft Azure Cognitive Services Translator REST APIs
    :param source_lang: autodetect language # source_lang: str,
    :param target_lang: language into which the translation is carried out
    :param text: text to be translated
    :return: translated text
    """

    key = os.environ.get("KEY_MICROSOFT")
    endpoint = "https://api.cognitive.microsofttranslator.com"

    location = os.environ.get("LOCATION")

    path = "/translate"
    constructed_url = endpoint + path

    params = {"api-version": "3.0", "to": [target_lang]}  # , "from": source_lang

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    print('response: ', response)
    translate = response[0]["detectedLanguage"]["language"], response[0]["translations"][0]["text"]
    return translate


if __name__ == "__main__":
    print(ms_translate(source_lang="en", target_lang="uk", text="duck"))
    print(ms_translate(source_lang="uk", target_lang="en", text="куче"))  # bg("куче") = en("dog")

    print('translate: ', ms_translate_auto(target_lang="en", text="куче"))
