from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
from repetitor_backend.settings.app import app_settings


DB = PostgresEngine(
    config={
        "database": app_settings.db.DB,
        "user": app_settings.db.USER,
        "password": app_settings.db.PASSWORD,
        "host": app_settings.db.HOST,
        "port": app_settings.db.PORT,
    }
)


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["repetitor_backend.piccolo_app", "repetitor_help.piccolo_app"])
