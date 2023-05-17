from pydantic import Field
from .db import ServiceDBSettings
from .base import AdvancedBaseSettings


class AppSettings(AdvancedBaseSettings):
    db = ServiceDBSettings()  # type: ignore
    ENV: str = Field(env="ENV", default="dev")
    URL_API_PREFIX: str = Field(env="URL_API_PREFIX", default="")

    def is_prod(self) -> bool:
        return self.ENV == "PROD"


app_settings = AppSettings()
print(f"app_sttings: {app_settings}")
