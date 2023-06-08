from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import UUID
from piccolo.columns.defaults.uuid import UUID4
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class ContentClass(Table, tablename="content_class"):
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


ID = "2023-05-26T21:49:19:262010"
VERSION = "0.111.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="repetitor_backend", description=DESCRIPTION
    )

    manager.rename_table(
        old_class_name="ContentClass",
        old_tablename="content_class",
        new_class_name="ContentType",
        new_tablename="content_type",
    )

    manager.alter_column(
        table_class_name="Context",
        tablename="context",
        column_name="context_class",
        db_column_name="context_class",
        params={"references": ContentType},
        old_params={"references": ContentClass},
        column_class=ForeignKey,
        old_column_class=ForeignKey,
    )

    return manager
