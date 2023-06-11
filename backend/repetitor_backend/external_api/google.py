import asyncio
from google.cloud import translate_v2 as translate

translate_client = translate.Client()


def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    return result


async def translate(target: str, text: str) -> dict:
    """Translate 'text' to language 'target' (ISO 639-1)."""
    result = await asyncio.to_thread(translate_text, target, text)
    return result
