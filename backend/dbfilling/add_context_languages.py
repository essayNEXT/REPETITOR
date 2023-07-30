"""The script is designed to fill the Context table with the appropriate ContextType.name = 'language'.

"""
import iso639
import requests
from typing import Dict
from repetitor_backend.external_api.google import translate_client
from repetitor_backend.tables import ContextType, Context

CONTEXT_TYPE_NAME = "language"
DESCRIPTION = "general kind of language for common uses (for examples: translater)"


def get_possible_google_lng() -> dict:
    """Return possibes languages for Google Translate.

    Format google (example):
        [
            {'language': 'ar', 'name': 'Arabic'},
            {'language': 'hy', 'name': 'Armenian'}.
            ...
            {'language': 'yi', 'name': 'Yiddish'},
            ...
        ]

    Reurn format:
    {
        'ar': 'Arabic',
        'hy': ''Armenian,
        ...
    }

    IMPORTANT:
        required keys and environment variable
        GOOGLE_APPLICATION_CREDENTIALS that points to the path to them
    """
    google_raw_results = translate_client.get_languages()
    google_res = {result["language"]: result["name"] for result in google_raw_results}
    print(f"all languages from Google: {len(google_res)}")
    return google_res


def get_possible_microsoft_lng(interface_lng: str = "en") -> dict:
    """Return possible languages for Microsoft translate.

    Format microsoft:
    {
        'af': {'name': 'Afrikaans', 'nativeName': 'Afrikaans', 'dir': 'ltr'},
        'am': {'name': 'Amharic', 'nativeName': 'አማርኛ', 'dir': 'ltr'},
        'ar': {'name': 'Arabic', 'nativeName': 'العربية', 'dir': 'rtl'},
        'as': {'name': 'Assamese', 'nativeName': 'অসমীয়া', 'dir': 'ltr'},
        'az': {'name': 'Azerbaijani', 'nativeName': 'Azərbaycan', 'dir': 'ltr'},
        'ba': {'name': 'Bashkir', 'nativeName': 'Bashkir', 'dir': 'ltr'},
        'bg': {'name': 'Bulgarian', 'nativeName': 'Български', 'dir': 'ltr'},
         ...
    }
    Return format:
    {
        'af': 'Afrikaans',
        'am': 'Amharic',
        ...
    }

    """
    params = {
        "api-version": "3.0",
        "scope": "translation",
    }  # scope = translation, transliteration, dictionary

    headers = {
        "Accept-Language": interface_lng,
    }
    URL_lNG = "https://api.cognitive.microsofttranslator.com/languages"

    response = requests.get(URL_lNG, params=params, headers=headers)
    response_data = response.json()

    microsoft_raw_results = response_data["translation"]
    microsoft_res = {
        result[0]: result[1]["name"] for result in microsoft_raw_results.items()
    }
    print(f"all languages from Microsoft: {len(microsoft_res)}")
    return microsoft_res


def get_all_iso639_form_if_possible(lng: str) -> set:
    """
    Returns a set of possible different values to describe this language
    (in the understanding of the iso639 standard).
    """
    try:
        lng_obj = iso639.Language.match(lng)
        lng_set = {
            el
            for el in (
                lng_obj.part1,
                lng_obj.part2t,
                lng_obj.part2b,
                lng_obj.part3,
                lng_obj.name,
            )
            if el
        }
    except iso639.LanguageNotFoundError:
        lng_set = {lng}
    return lng_set


def get_lng_existing_in_db(context_type: str = CONTEXT_TYPE_NAME) -> set:
    """Returns a set consisting of short descriptions (Context.name_short) of the
    languages that exist in the database.
    """
    # Get ContextType.id
    context_type_id = (
        ContextType.select(ContextType.id)
        .where(ContextType.name == CONTEXT_TYPE_NAME)
        .run_sync()
    )
    context_type_id = context_type_id[0]["id"]
    # get existing languages in DB
    existing_in_db_languages = (
        Context.select(Context.name_short)
        .where(Context.context_type == context_type_id)
        .run_sync()
    )
    in_db_set = set([lng["name_short"] for lng in existing_in_db_languages])
    print(f"all languages in DB: {len(in_db_set)}")
    return in_db_set


def get_nessesary_to_add(
    possible_from_translator: Dict[str, str], existing_in_db: set
) -> Dict[str, str]:
    """Compare all existing  languages in DB  with  new translator`s languages and return dict
    for adding (a comparison according any iso639 form).
    """
    to_add = {
        name_short: name
        for name_short, name in possible_from_translator.items()
        if not (get_all_iso639_form_if_possible(name_short) & existing_in_db)
    }
    print(f"total languages to add: {len(to_add)}")
    for name_short, name in to_add.items():
        print(f"--> {name_short:>10} - {name:<20}")
    return to_add


def add_to_db_new_languages(
    necessary_to_add: dict,
    context_type_name: str = CONTEXT_TYPE_NAME,
    description: str = DESCRIPTION,
) -> None:
    """Adds to the database the languages listed in the
    'necessary_to_add' parameter - name, name_short.
    """
    # Get ContextType.id
    context_type_id = (
        ContextType.select(ContextType.id)
        .where(ContextType.name == context_type_name)
        .run_sync()
    )
    context_type_id = context_type_id[0]["id"]
    if necessary_to_add:
        name_short, name = necessary_to_add.popitem()
        query = Context.insert(
            Context(
                context_type=context_type_id,
                name=name,
                name_short=name_short,
                description=DESCRIPTION,
            )
        )
        for name_short, name in necessary_to_add.items():
            query.add(
                Context(
                    context_type=context_type_id,
                    name=name,
                    name_short=name_short,
                    description=DESCRIPTION,
                )
            )
        query.run_sync()
