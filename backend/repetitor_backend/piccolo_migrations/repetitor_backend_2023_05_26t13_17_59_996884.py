from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Email
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import UUID
from piccolo.columns.column_types import Varchar
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


ID = "2023-05-26T13:17:59:996884"
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

    manager.drop_column(
        table_class_name="CustomerType",
        tablename="customer_type",
        column_name="describe",
        db_column_name="describe",
    )

    manager.add_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="email",
        db_column_name="email",
        column_class_name="Email",
        column_class=Email,
        params={
            "length": 255,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="native_language",
        db_column_name="native_language",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 20,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="tlg_first_name",
        db_column_name="tlg_first_name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 50,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="tlg_last_name",
        db_column_name="tlg_last_name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 50,
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="CustomerType",
        tablename="customer_type",
        column_name="description",
        db_column_name="description",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 200,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.rename_column(
        table_class_name="Customer",
        tablename="customer",
        old_column_name="telegram_language",
        new_column_name="tlg_language",
        old_db_column_name="telegram_language",
        new_db_column_name="tlg_language",
    )

    manager.rename_column(
        table_class_name="Customer",
        tablename="customer",
        old_column_name="telegram_user_id",
        new_column_name="tlg_user_id",
        old_db_column_name="telegram_user_id",
        new_db_column_name="tlg_user_id",
    )

    manager.rename_column(
        table_class_name="Customer",
        tablename="customer",
        old_column_name="user_name",
        new_column_name="tlg_user_name",
        old_db_column_name="user_name",
        new_db_column_name="tlg_user_name",
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

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="first_name",
        db_column_name="first_name",
        params={"lenght": 50, "length": 255, "null": True},
        old_params={"lenght": None, "length": 50, "null": False},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="last_name",
        db_column_name="last_name",
        params={"lenght": 50, "length": 255},
        old_params={"lenght": None, "length": 50},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    manager.alter_column(
        table_class_name="CustomerType",
        tablename="customer_type",
        column_name="name",
        db_column_name="name",
        params={"unique": True},
        old_params={"unique": False},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    return manager
