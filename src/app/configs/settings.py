from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .external_settings import ExternalSettings
from .internal_settings import InternalSettings


class Settings(BaseSettings):
    internal: InternalSettings = Field(default_factory=InternalSettings)
    external: ExternalSettings = Field(default_factory=ExternalSettings)

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="PMT__",
        case_sensitive=False,
        extra="ignore",
    )
