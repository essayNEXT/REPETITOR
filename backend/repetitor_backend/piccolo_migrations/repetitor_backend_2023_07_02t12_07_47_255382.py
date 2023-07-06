from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import BigInt


ID = "2023-07-02T12:07:47:255382"
VERSION = "0.111.1"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="repetitor_backend", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="tlg_user_id",
        db_column_name="tlg_user_id",
        params={"unique": True},
        old_params={"unique": False},
        column_class=BigInt,
        old_column_class=BigInt,
    )

    return manager
