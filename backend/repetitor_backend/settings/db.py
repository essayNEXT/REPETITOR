from .base import AdvancedBaseSettings
from pydantic import Field


class ServiceDBSettings(AdvancedBaseSettings):
    HOST: str = Field(default="repetitor_db")
    USER: str = Field(defaulf="repetitor_back")
    PASSWORD: str = Field(defaulf="__back")
    DB: str = Field(defaulf="REPETITOR")
    PORT: int = Field(default="5432")

    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def postgresql_url(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
