from .base import AdvancedBaseSettings
import os


class ServiceDBSettings(AdvancedBaseSettings):
    HOST: str = os.environ.get("POSTGRES_HOST", default="localhost")
    USER: str = os.environ.get("POSTGRES_USER", default="repetitor_back")
    PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", default="__back")
    DB: str = os.environ.get("POSTGRES_DB", default="REPETITOR")
    PORT: int = int(os.environ.get("POSTGRES_PORT", default=5433))

    class Config:
        env_prefix = "POSTGRES_"
        env_file_encoding = "utf-8"

    @property
    def postgresql_url(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
