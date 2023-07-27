from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import UUID
from piccolo.columns.defaults.uuid import UUID4
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class ContentType(Table, tablename="content_type"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


class ContextType(Table, tablename="context_type"):
    id = UUID(
        default=UUID4(),
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


ID = "2023-05-27T13:50:01:850771"
VERSION = "0.111.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="repetitor_backend", description=DESCRIPTION
    )

    manager.rename_table(
        old_class_name="ContentType",
        old_tablename="content_type",
        new_class_name="ContextType",
        new_tablename="context_type",
    )

    manager.alter_column(
        table_class_name="Context",
        tablename="context",
        column_name="context_class",
        db_column_name="context_class",
        params={"references": ContextType},
        old_params={"references": ContentType},
        column_class=ForeignKey,
        old_column_class=ForeignKey,
    )

    return manager
