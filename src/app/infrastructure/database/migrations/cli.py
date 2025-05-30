import os
from urllib.parse import urlparse, urlunparse

import typer

from app.infrastructure.database.migrations.config import AlembicConfig
from app.infrastructure.database.migrations.manager import AlembicManager

app = typer.Typer(help="CLI for Migrations")


def patch_sqlalchemy_url(url: str) -> str:
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    new_scheme = scheme

    if scheme == "postgresql":
        new_scheme = "postgresql+psycopg"

    if new_scheme != scheme:
        return urlunparse((new_scheme, *parsed[1:]))  # noqa
    return url


def resolve_database_url(database_url: str | None) -> str:
    if database_url:
        return patch_sqlalchemy_url(database_url)

    env_url = os.getenv("MIGRATIONS_URL_DATABASE")
    if env_url:
        return patch_sqlalchemy_url(env_url)

    raise typer.BadParameter(
        "Database URL not provided. Use --database-url option or set MIGRATIONS_URL_DATABASE environment variable."
    )


@app.command()
def revision(
    message: str = typer.Option(..., "--message", "-m", help="Revision message"),
    autogenerate: bool = typer.Option(True, help="Autogenerate the migration"),
    database_url: str = typer.Option(None, help="Database URL"),
) -> None:
    url = resolve_database_url(database_url)
    manager = AlembicManager(AlembicConfig(url))
    manager.create_revision(message=message, autogenerate=autogenerate)
    typer.secho("Revision created successfully.", fg=typer.colors.GREEN)


@app.command()
def upgrade(
    revision: str = typer.Argument("head", help="Revision to upgrade to"),  # noqa
    database_url: str = typer.Option(None, help="Database URL"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
) -> None:
    if not yes:
        confirm = typer.confirm("Are you sure you want to perform the upgrade?")
        if not confirm:
            typer.secho("Upgrade cancelled.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=0)

    url = resolve_database_url(database_url)
    manager = AlembicManager(AlembicConfig(url))
    manager.apply_migrations(revision=revision)
    typer.secho(
        f"Upgrade to revision '{revision}' completed successfully.",
        fg=typer.colors.GREEN,
    )


@app.command()
def downgrade(
    revision: str = typer.Argument("-1", help="Revision to downgrade to"),  # noqa
    database_url: str = typer.Option(None, help="Database URL"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
) -> None:
    if not yes:
        confirm = typer.confirm("Are you sure you want to perform the upgrade?")
        if not confirm:
            typer.secho("Upgrade cancelled.", fg=typer.colors.YELLOW)
            raise typer.Exit(code=0)

    url = resolve_database_url(database_url)
    manager = AlembicManager(AlembicConfig(url))
    manager.downgrade_migrations(revision=revision)
    typer.secho(
        f"Downgrade to revision '{revision}' completed successfully.",
        fg=typer.colors.GREEN,
    )


@app.command()
def current(database_url: str = typer.Option(None, help="Database URL")) -> None:
    url = resolve_database_url(database_url)
    manager = AlembicManager(AlembicConfig(url))
    manager.show_current_revision()


@app.command()
def history(database_url: str = typer.Option(None, help="Database URL")) -> None:
    url = resolve_database_url(database_url)
    manager = AlembicManager(AlembicConfig(url))
    manager.show_history()


if __name__ == "__main__":
    app()
