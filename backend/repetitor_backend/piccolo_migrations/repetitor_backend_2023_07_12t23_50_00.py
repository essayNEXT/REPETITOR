from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.table import Table


class RawTable(Table):
    pass


ID = "2023-07-12T23:50:00"
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
            """ insert into customer (id, customer_class, tlg_user_id, tlg_first_name, tlg_language, is_active)
            VALUES
        ('00000000-0000-0000-0000-000000000000', 'translator', '0', 'microsoft_translate', 'en', true),
        ('00000000-0000-0000-0000-000000000001', 'translator', '1', 'google_translate', 'en', true);
        insert into explanation(id, description, is_active)
        VALUES
        ('00000000-0000-0000-0000-000000000010','word translation', true);
        insert into relation_type (id, name, is_active)
        VALUES
        ('00000000-0000-0000-0000-000000000020','word translation', true);
        """
        )

        await RawTable.raw(
            """ ALTER TABLE customer_context DROP CONSTRAINT unique_combination_cc;
                create unique index customer_context_idx
                on customer_context (greatest(customer,context_1,context_2), least(customer,context_1,context_2));
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
