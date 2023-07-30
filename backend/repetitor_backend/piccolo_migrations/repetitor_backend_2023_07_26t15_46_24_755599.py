from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from dbfilling.add_contexttype import add_contexttype
from dbfilling.add_context_languages import (
    get_lng_existing_in_db,
    get_possible_google_lng,
    get_possible_microsoft_lng,
    add_to_db_new_languages,
    get_nessesary_to_add,
)


ID = "2023-07-26T15:46:24:755599"
VERSION = "0.111.0"
DESCRIPTION = "Adding content_type: language, add: context for context_type=language googles possible languages"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="", description=DESCRIPTION)

    def run():
        print(f"running {ID}")
        # create context_type: langiage
        context_types = {
            "language": "The base type for languages that are available to all users without restrictions.",
        }
        add_contexttype(context_types=context_types)

        # add google`s possible languages
        existing_in_db_lng_set = get_lng_existing_in_db()
        possible_google_lng = get_possible_google_lng()
        nessesary_to_add_dict = get_nessesary_to_add(
            possible_from_translator=possible_google_lng,
            existing_in_db=existing_in_db_lng_set,
        )
        add_to_db_new_languages(necessary_to_add=nessesary_to_add_dict)

        # add microsoft`s possible languages
        existing_in_db_lng_set = get_lng_existing_in_db()
        possible_microsoft_lng = get_possible_microsoft_lng()
        nessesary_to_add_dict = get_nessesary_to_add(
            possible_from_translator=possible_microsoft_lng,
            existing_in_db=existing_in_db_lng_set,
        )
        add_to_db_new_languages(necessary_to_add=nessesary_to_add_dict)

    manager.add_raw(run)

    return manager
