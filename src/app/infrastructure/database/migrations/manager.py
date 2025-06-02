from alembic import command

from app.infrastructure.database.migrations.config import AlembicConfig


class AlembicManager:
    def __init__(self, alembic_cfg: AlembicConfig) -> None:
        self.alembic_config_obj = alembic_cfg
        self.alembic_actual_config = self.alembic_config_obj()

    def create_revision(self, message: str, autogenerate: bool = True) -> None:
        try:
            command.revision(self.alembic_actual_config, message=message, autogenerate=autogenerate)
        except Exception as e:
            raise RuntimeError("Failed to create revision") from e

    def apply_migrations(self, revision: str = "head") -> None:
        try:
            command.upgrade(self.alembic_actual_config, revision)
        except Exception as e:
            raise RuntimeError(f"Failed to apply migrations up to {revision}") from e

    def downgrade_migrations(self, revision: str = "-1") -> None:
        try:
            command.downgrade(self.alembic_actual_config, revision)
        except Exception as e:
            raise RuntimeError(f"Failed to downgrade to revision {revision}") from e

    def show_current_revision(self) -> None:
        try:
            command.current(self.alembic_actual_config, verbose=True)
        except Exception as e:
            raise RuntimeError("Failed to show current revision") from e

    def show_history(self) -> None:
        try:
            command.history(self.alembic_actual_config)
        except Exception as e:
            raise RuntimeError("Failed to show migration history") from e
