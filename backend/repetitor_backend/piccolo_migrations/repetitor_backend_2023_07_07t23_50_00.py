from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.table import Table


class RawTable(Table):
    pass


ID = "2023-07-07T23:50:00"
VERSION = "0.111.1"
DESCRIPTION = "RTM"


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="repetitor_backend", description=DESCRIPTION
    )

    #############################################################
    # This will get run when using `piccolo migrations forwards`:

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

        await RawTable.raw(
            """
                ALTER TABLE customer_context
                  ADD CONSTRAINT unique_combination_cc UNIQUE (customer, context_1, context_2);
        """
        )

    manager.add_raw(run)

    #############################################################
    # If we want to run some code when reversing the migration,
    # using `piccolo migrations backwards`:

    async def run_backwards():
        await RawTable.raw("""DROP VIEW item_relation_view;""")

        await RawTable.raw(
            """ALTER TABLE question DROP CONSTRAINT unique_combination_q;"""
        )

        await RawTable.raw(
            """ALTER TABLE right_answ_item DROP CONSTRAINT unique_combination_rai;"""
        )

        await RawTable.raw("""ALTER TABLE item DROP CONSTRAINT unique_combination_i;""")

        await RawTable.raw(
            """ALTER TABLE customer_context DROP CONSTRAINT unique_combination_cc;"""
        )

    manager.add_raw_backwards(run_backwards)

    #############################################################
    # We must always return the MigrationManager:

    return manager
