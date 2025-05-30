import abc

from .aClasses import ASQLDatabase


class APostgresDatabase(ASQLDatabase, abc.ABC):
    def __init__(self, user: str, password: str, host: str, port: int, database: str, automigrate: bool):
        driver = "postgresql+psycopg"
        super().__init__(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            driver=driver,
            automigrate=automigrate,
        )


class PostgresDatabase(APostgresDatabase):
    def __init__(self, user: str, password: str, host: str, port: int, database: str, automigrate: bool):
        super().__init__(user=user, password=password, host=host, port=port, database=database, automigrate=automigrate)
