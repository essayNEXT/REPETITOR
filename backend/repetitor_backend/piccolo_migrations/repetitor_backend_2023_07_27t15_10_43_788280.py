from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.table import Table

ID = "2023-07-27T15:10:43:788280"
VERSION = "0.111.0"
DESCRIPTION = """Initial filling of the database - adding to the table CustomerType of values ​​for
                the translator and ordinary user, adding translator users to the table
                Customer - Google and Microsoft
              """


class RawTable(Table):
    pass


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
            """ insert into customer (id, customer_type, tlg_user_id, tlg_first_name, tlg_language, is_active)
            VALUES
('00000000-0000-0000-0000-000000000000', '10000000-0000-0000-0000-000000000000', '0', 'microsoft_translate', 'en', true)
        """
        )

        await RawTable.raw(
            """ insert into customer (id, customer_type, tlg_user_id, tlg_first_name, tlg_language, is_active)
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

    manager.add_raw(run)

    #############################################################
    # We must always return the MigrationManager:

    return manager
