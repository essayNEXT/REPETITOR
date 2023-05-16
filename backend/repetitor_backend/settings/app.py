from pydantic import BaseSettings
from .db import ServiceDBSettings


class AppSettings(BaseSettings):
    db = ServiceDBSettings()  # type: ignore


app_settings = AppSettings()
print(f"app_sttings: {app_settings}")
