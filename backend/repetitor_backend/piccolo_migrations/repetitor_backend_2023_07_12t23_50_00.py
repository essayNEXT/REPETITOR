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
            """ insert into customer_type (id, name, description, is_active)
            VALUES
        ('10000000-0000-0000-0000-000000000000', 'translator', 'trusted translate customer', true)
        """
        )

        await RawTable.raw(
            """ insert into customer_type (id, name, description, is_active)
            VALUES
        ('10000000-0000-0000-0000-000000000001', 'user', 'normal customer', true)
        """
        )

        await RawTable.raw(
            """ insert into customer (id, customer_class, tlg_user_id, tlg_first_name, tlg_language, is_active)
            VALUES
('00000000-0000-0000-0000-000000000000', '10000000-0000-0000-0000-000000000000', '0', 'microsoft_translate', 'en', true)
        """
        )

        await RawTable.raw(
            """ insert into customer (id, customer_class, tlg_user_id, tlg_first_name, tlg_language, is_active)
            VALUES
('00000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000000', '1', 'google_translate', 'en', true)
        """
        )

        await RawTable.raw(
            """ insert into explanation(id, description, is_active)
        VALUES
        ('00000000-0000-0000-0000-000000000010','word translation', true);
        """
        )

        await RawTable.raw(
            """insert into relation_type (id, name, is_active)
        VALUES
        ('00000000-0000-0000-0000-000000000020','word translation', true);
        """
        )

        await RawTable.raw(
            """ ALTER TABLE customer_context DROP CONSTRAINT unique_combination_cc;
        """
        )

    manager.add_raw(run)

    #############################################################
    # We must always return the MigrationManager:

    return manager