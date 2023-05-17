from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2023-05-17T17:16:01:890314"
VERSION = "0.111.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
