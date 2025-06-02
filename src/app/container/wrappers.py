from app.configs import Settings
from app.infrastructure import PostgresDatabase


class PostgresDatabaseWrapper(PostgresDatabase):
    def __init__(self, settings: Settings):
        pg = settings.external.postgres
        super().__init__(
            user=pg.user,
            password=pg.password,
            host=pg.host,
            port=pg.port,
            database=pg.database,
            automigrate=pg.automigrate,
        )
