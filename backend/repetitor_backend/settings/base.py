from pathlib import Path

from pydantic import BaseSettings


BASE_DIRECTORY = Path(__file__).absolute().parent.parent.parent


class AdvancedBaseSettings(BaseSettings):
    """Base object with common settings."""

    class Config:
        case_sensitive = True
        allow_mutation = False  # This setting makes the object immutable.
