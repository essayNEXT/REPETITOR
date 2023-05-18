from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import UUID
from piccolo.columns.defaults.uuid import UUID4
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class CustomerClass(Table, tablename="customer_class"):
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


class CustomerType(Table, tablename="customer_type"):
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


ID = "2023-05-18T12:32:46:956090"
VERSION = "0.111.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="repetitor_backend", description=DESCRIPTION
    )

    manager.rename_table(
        old_class_name="CustomerClass",
        old_tablename="customer_class",
        new_class_name="CustomerType",
        new_tablename="customer_type",
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="customer_class",
        db_column_name="customer_class",
        params={"references": CustomerType},
        old_params={"references": CustomerClass},
        column_class=ForeignKey,
        old_column_class=ForeignKey,
    )

    return manager
