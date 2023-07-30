from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.table import Table


ID = "2023-07-23T17:07:11:273590"
VERSION = "0.111.0"
DESCRIPTION = "Create view item_relation_view and adding restrictions."


class RawTable(Table):
    pass


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="", description=DESCRIPTION)

    async def run():
        await RawTable.raw(
            """
            CREATE VIEW item_relation_view AS
            SELECT ir1.id as item_relation, i1."text" as item_text_1, i1.author as item_author_1,
                                            c1.name_short as item_context_name_short_1,
                                            i2."text" as item_text_2, i2.author as item_author_2,
                                            c2.name_short as item_context_name_short_2,
                                            q1.id as question, rai2.id as right_answ_item, ir1.is_active  as is_active
            FROM item i1
            JOIN context c1 ON i1.context = c1.id
            JOIN question q1 ON q1.item = i1.id
            JOIN item_relation ir1 ON ir1.id = q1.relation
            JOIN right_answ_item rai2 ON ir1.id =  rai2.relation
            JOIN item i2 ON i2.id = rai2.item
            JOIN context c2 ON i2.context = c2.id
            ;
        """
        )

        await RawTable.raw(
            """
                ALTER TABLE question
                  ADD CONSTRAINT unique_combination_q UNIQUE (relation, item);
        """
        )

        await RawTable.raw(
            """
                ALTER TABLE right_answ_item
                  ADD CONSTRAINT unique_combination_rai UNIQUE (relation, item);
        """
        )

        await RawTable.raw(
            """
                ALTER TABLE item
                  ADD CONSTRAINT unique_combination_i UNIQUE (text, author, context);
        """
        )

    manager.add_raw(run)

    async def run_backwards():
        await RawTable.raw("""DROP VIEW item_relation_view;""")

        await RawTable.raw(
            """ALTER TABLE question DROP CONSTRAINT unique_combination_q;"""
        )

        await RawTable.raw(
            """ALTER TABLE right_answ_item DROP CONSTRAINT unique_combination_rai;"""
        )

        await RawTable.raw("""ALTER TABLE item DROP CONSTRAINT unique_combination_i;""")

    manager.add_raw_backwards(run_backwards)

    return manager
