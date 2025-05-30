from pydantic import BaseModel, Field


class PostgresSettings(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=5432)
    database: str = Field(default="python_microservice_templates")
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    automigrate: bool = Field(default=True)


class ExternalSettings(BaseModel):
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
