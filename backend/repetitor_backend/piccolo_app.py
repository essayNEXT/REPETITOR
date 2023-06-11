import os

from piccolo.conf.apps import AppConfig
from .tables import (
    CustomerType,
    Customer,
    ContextType,
    Context,
    CustomerContext,
    Item,
    Explanation,
    RelationType,
    ItemRelation,
    WrongAnswItem,
    RightAnswItem,
    Question,
    Cards,
)

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

APP_CONFIG = AppConfig(
    app_name="repetitor_backend",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=[CustomerType, Customer, ContextType, Context, CustomerContext, Item, Explanation, RelationType,
                   ItemRelation, WrongAnswItem, RightAnswItem, Question, Cards
                   ],
    migration_dependencies=[],
    commands=[],
)
