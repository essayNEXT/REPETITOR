"""The script is designed to fill the Context table with the appropriate ContextType.name = 'language'.

"""
from typing import List
import iso639
from repetitor_backend.external_api.google import translate_client
from repetitor_backend.tables import ContextType, Context

CONTEXT_TYPE_NAME = "language"
DESCRIPTION = "general language"


def get_short_and_name(
    name: iso639.Language | str, possible_google_languages_full: List[dict]
) -> tuple:
    if isinstance(name, iso639.Language):
        return (
            name.part1 or name.part2b or name.part2t or name.part3 or name.name,
            name.name,
        )
    return [
        (elem["language"] or elem["name"], elem["name"])
        for elem in possible_google_languages_full
        if elem["name"] == name
    ][0]


# Get ContextType.id
context_type_id = (
    ContextType.select(ContextType.id)
    .where(ContextType.name == CONTEXT_TYPE_NAME)
    .run_sync()
)
context_type_id = context_type_id[0]["id"]
# print(f"ContextType.id: {context_type_id}")

# get new languages from Google:
possible_google_languages_full = translate_client.get_languages()
possible_google_languages = [lng["name"] for lng in possible_google_languages_full]

# get existing languages in DB
existing_in_db_languages = (
    Context.select(Context.name)
    .where(Context.context_class == context_type_id)
    .run_sync()
)

# To compare existing and new language contexts, we use the iso639.Languagee object (documentation
# here - https://pypi.org/project/python-iso639/). This will minimize confusion with different descriptions
# (in different standards) of the same language.
# Since there may be non-standardized descriptions of languages in various APIs, the following algorithm is used
# to resolve this situation:
# - for new languages added to the database, if a non-standardized name is found, a message about this is
# displayed in the console, the received name of the language is displayed and the operator is invited to
# independently make a decision (daenet) on entering this language into valid contexts
# - for non-standardized descriptions of languages existing in the database (previously entered), they are
# compared with the introduced languages simply as string objects.

# Match both lists of languages in iso639.Language objects
set_existing_in_db_languages = set()
for lng in existing_in_db_languages:
    try:
        lang_obj = iso639.Language.match(lng)
        set_existing_in_db_languages.add(lang_obj)
    except iso639.LanguageNotFoundError:
        set_existing_in_db_languages.add(lng)

set_possible_google_languages = set()
for lng in possible_google_languages:
    try:
        lang_obj = iso639.Language.match(lng)
        set_possible_google_languages.add(lang_obj)
    except iso639.LanguageNotFoundError:
        print(
            f"The language object you want to add as cotext has a non-standardized (iso639) name: {lng}"
        )
        inp = input("add to DB? (yes/no)")
        if inp in ("YES", "yes", "Yes", "Y", "y"):
            set_possible_google_languages.add(lng)


# for adding to DB:
set_to_db = set_possible_google_languages - set_existing_in_db_languages
if set_to_db:
    elem = set_to_db.pop()
    name_short, name = get_short_and_name(elem, possible_google_languages_full)
    query = Context.insert(
        Context(
            context_class=context_type_id,
            name=name,
            name_short=name_short,
            description=DESCRIPTION,
        )
    )
    while set_to_db:
        elem = set_to_db.pop()
        name_short, name = get_short_and_name(elem, possible_google_languages_full)
        query = query.add(
            Context(
                context_class=context_type_id,
                name=name,
                name_short=name_short,
                description=DESCRIPTION,
            )
        )
    query.run_sync()
