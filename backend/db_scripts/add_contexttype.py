"""This script must be run once when creating the database to add the required context types.

all added types must be described as a dict, where each pair key:value describes one type of context: the
key is the name of the context (string, maximum length 20 characters, must be unique), and the value is a
description of the context (string, required, restrictions no length):

context_types = {
    "name_1": "description_1",
    "name_2": "description_2",
    ...,
    "name_n": "description_n",
    }

Before attempting to add a list of context_types to the database table (ContextType), all existing records
are read from this table, a check is made for the existence in the table of values ContextType.name. If such ones
already exist, they are not entered into the table; a message is generated about this.
"""

from repetitor_backend.tables import ContextType


context_types = {
    "language": "The base type for languages that are available to all users without restrictions.",
}

existing_context_names = ContextType.select(ContextType.name).run_sync()
set_existing_context_names = {
    context_type_name["name"] for context_type_name in existing_context_names
}
set_context_types = set(context_types)

exist_in_db_and_in_context_types_dict = set_context_types & set_existing_context_names
if exist_in_db_and_in_context_types_dict:
    print("already exist in the database (will not be added):")
    for name in exist_in_db_and_in_context_types_dict:
        print(f"-> name: {name}, --> describe: {context_types[name]}")

to_add_to_db = set_context_types - set_existing_context_names
if to_add_to_db:
    print("-" * 120)
    print("new ContextType records will be added to the database:")
    for name in to_add_to_db:
        print(f"-> name: {name}, --> describe: {context_types[name]}")

    name = to_add_to_db.pop()
    query = ContextType.insert(ContextType(name=name, description=context_types[name]))
    while to_add_to_db:
        name = to_add_to_db.pop()
        query = query.add(ContextType(name=name, description=context_types[name]))
    query.run_sync()
    print("new ContextType added in DB.")
    print("-" * 120)
