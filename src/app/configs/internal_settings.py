from pydantic import BaseModel, Field

from app.logs import LogLevel


class LogsSettings(BaseModel):
    enable: bool = Field(default=True)
    level: LogLevel = Field(default=LogLevel.INFO)


class InternalSettings(BaseModel):
    log: LogsSettings = Field(default_factory=LogsSettings)
