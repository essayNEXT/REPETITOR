import os

from piccolo.conf.apps import AppConfig
from .tables import (
    Customer,
    CustomerType,
    ContentClass, Content
)


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


APP_CONFIG = AppConfig(
    app_name="repetitor_backend",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=[Customer, CustomerType, ContentClass, Content],
    migration_dependencies=[],
    commands=[],
)
