from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar


ID = "2023-05-26T13:47:51:473263"
VERSION = "0.111.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="repetitor_backend", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="native_language",
        db_column_name="native_language",
        params={"length": 10},
        old_params={"length": 20},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    return manager
