from alembic.config import Config

from app.infrastructure.database.migrations import MIGRATIONS_LOCATION_PATH


class AlembicConfig:
    def __init__(self, database_url: str):
        self.config = Config()
        self.config.set_main_option("script_location", str(MIGRATIONS_LOCATION_PATH))
        self.config.set_main_option("sqlalchemy.url", database_url)

    def __call__(self) -> Config:
        return self.config
