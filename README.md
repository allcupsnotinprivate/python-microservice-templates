# 🐍 Python Microservice Templates

## 🚀 Overview

**Python Microservice Templates** is a production-ready template for building asynchronous REST microservices using 
FastAPI. It comes pre-configured with PostgreSQL, SQLAlchemy, Alembic for database migrations, background task scheduling 
via APScheduler, and Docker support. It’s ideal for quickly bootstrapping microservice-based APIs and background workers.

## ✨ Features

* ✅ **FastAPI** — a modern, high-performance web framework for building APIs.
* 📦 **PostgreSQL** with the asynchronous `psycopg` driver and SQLAlchemy 2.0 ORM.
* 🧠 **Dependency injection** powered by `aioinject`.
* ⚙️ **Alembic** — built-in database migration support.
* ⏱️ **APScheduler** — schedule background tasks using cron/date/interval triggers.
* 🐳 **Docker-ready** — supports both dev and production container builds.
* 🧪 Unified quality checks with **type-checking** (`mypy`), **linting** (`ruff`), and **security** (`bandit`).
* 🎯 Based on **Python 3.12** with strict typing configuration.
* 🧩 Pre-structured for adding REST endpoints (e.g., `conversations`) and background jobs.

## 🛠️ Tech Stack

| Layer            | Technology                                                                                                                                                                           |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Language         | [Python 3.12](https://www.python.org/downloads/release/python-3120/)                                                                                                                 |
| Web Framework    | [FastAPI](https://fastapi.tiangolo.com/)                                                                                                                                             |
| Database         | [PostgreSQL](https://www.postgresql.org/)                                                                                                                                            |
| ORM              | [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)                                                                                                                                 |
| Migrations       | [Alembic](https://alembic.sqlalchemy.org/)                                                                                                                                           |
| Scheduler        | [APScheduler](https://apscheduler.readthedocs.io/en/latest/)                                                                                                                         |
| DI Container     | [aioinject](https://pypi.org/project/aioinject/)                                                                                                                                     |
| Async Runtime    | [Uvicorn](https://www.uvicorn.org/)                                                                                                                                                  |
| Dev Tools        | [Rye](https://rye-up.com/), [Hatch](https://hatch.pypa.io/), [Ruff](https://docs.astral.sh/ruff/), [Mypy](http://mypy-lang.org/), [Bandit](https://bandit.readthedocs.io/en/latest/) |
| Packaging        | [Hatchling](https://hatch.pypa.io/latest/build/)                                                                                                                                     |
| Containerization | [Docker](https://www.docker.com/)                                                                                                                                                    |

---

Вот заполненный раздел **Getting Started** на английском языке, включая требования, установку и запуск:

---

## 🏁 Getting Started

### 🧰 Prerequisites

Make sure you have the following tools installed on your system:

* [Python 3.12+](https://www.python.org/downloads/release/python-3120/)
* [Docker](https://www.docker.com/)
* [Rye](https://rye-up.com/) (Python project management tool)

  * To install Rye:

    ```bash
    curl -sSf https://rye-up.com/get | bash
    ```

> ℹ️ Optionally, [Poetry](https://python-poetry.org/) or [Hatch](https://hatch.pypa.io/) can be used, but this project is configured for [Rye](https://rye-up.com/).

---

### 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/allcupsnotinprivate/python-microservice-templates.git
cd python-microservice-templates

# Sync the environment using Rye
rye sync
```

Create and configure your environment variables file (e.g., `.dev.env`). You can start with a copy of the provided example:

```bash
cp .env.example .dev.env
```

---

### ▶️ Running the App

#### With Rye

```bash
# Run the FastAPI app with Uvicorn
rye run asgi
```

#### With Docker

Make sure Docker is installed and running, then:

```bash
# Build and start the containers
docker-compose -f deploy/docker-compose.yml -p pmt up -d
```

The app should now be accessible at [http://localhost:8000](http://localhost:8000)

---

## 🔧 Environment Configuration

The environment is configured using environment variables with the prefix `PMT__`. The configuration is loaded via 
`pydantic-settings` and supports nested settings using the double underscore `__` delimiter.

Main PostgreSQL connection variables:

| Variable                               | Description                           | Example value                      |
|----------------------------------------|---------------------------------------|------------------------------------|
| `PMT__EXTERNAL__POSTGRES__HOST`        | Database host                         | `localhost` or `database` (docker) |
| `PMT__EXTERNAL__POSTGRES__PORT`        | Database port                         | `5432`                             |
| `PMT__EXTERNAL__POSTGRES__DATABASE`    | Database name                         | `python_microservice_templates`    |
| `PMT__EXTERNAL__POSTGRES__USER`        | Database user                         | `postgres`                         |
| `PMT__EXTERNAL__POSTGRES__PASSWORD`    | Database password                     | `postgres`                         |
| `PMT__EXTERNAL__POSTGRES__AUTOMIGRATE` | Whether to run auto migrations (bool) | `true` (default) or `false`        |

You can use a `.env` file with the following content (check `.env.example`):

```env
PMT__EXTERNAL__POSTGRES__HOST=database
PMT__EXTERNAL__POSTGRES__PORT=5432
PMT__EXTERNAL__POSTGRES__DATABASE=python_microservice_templates
PMT__EXTERNAL__POSTGRES__USER=postgres
PMT__EXTERNAL__POSTGRES__PASSWORD=postgres
PMT__EXTERNAL__POSTGRES__AUTOMIGRATE=true
```

These environment variables are loaded automatically when running the app or migration CLI.

---

## 🗄️ Database & Migrations

### ⚙️ Initializing the Database
The database service is configured in `docker-compose.yml` with PostgreSQL running and ready to use with the default 
credentials:
- User: `postgres`
- Password: `postgres`
- Database: `python_microservice_templates`

The database data is persisted in the Docker volume `database_data`.

---

### 🧩 Running Migrations

This project uses **Alembic** for database migrations, wrapped by a `typer` CLI located at:

```
src/app/infrastructure/database/migrations/cli.py
```

You can run migration commands directly using:

```bash
python src/app/infrastructure/database/migrations/cli.py <command> [options]
```

For convenience, the migration CLI is registered as a **Rye** script, so you can also invoke it via Rye’s task runner:

```bash
rye run migrations <command> [options]
```

---

#### Database URL Configuration

By default, the CLI reads the database connection URL from the environment variable:

```env
MIGRATIONS_URL_DATABASE
```

The URL should be in the standard SQLAlchemy format, e.g.:

```
postgresql://postgres:postgres@localhost:5432/python_microservice_templates
```

If needed, you can override this URL per command by providing the `--database-url` option:

```bash
rye run migrations <command> --database-url postgresql://postgres:postgres@localhost:5432/python_microservice_templates
```

---

#### Available Commands

##### Create a Migration Revision (with Autogeneration)

Creates a new migration revision file. By default, Alembic will attempt to **autogenerate** the migration by comparing models to the database schema.

```bash
rye run migrations revision -m "Add new users table"
```

You can disable autogeneration by passing `--autogenerate false` if you want to write migrations manually.

---

##### Apply Migrations (Upgrade)

Applies migrations to bring your database schema **up** to the specified revision (defaults to the latest, `head`).

```bash
rye run migrations upgrade
```

> **Interactive confirmation:**  
> Before applying migrations, the CLI will prompt for confirmation:  
> `Are you sure you want to perform the upgrade? [y/N]: ...`
>
> To skip this prompt (e.g., in CI pipelines or automated scripts), use the `-y` or `--yes` flag:
>
> ```bash
> rye run migrations upgrade -y
> ```

---

##### Roll Back Migrations (Downgrade)

Rolls back migrations **down** to the specified revision (defaults to one step down, `-1`).

```bash
rye run migrations downgrade
```

> **Interactive confirmation:**  
> Before rolling back migrations, the CLI will prompt:  
> `Are you sure you want to perform the upgrade? [y/N]: ...`  
> (Yes, this message is reused but means downgrade confirmation.)
>
> To skip the confirmation prompt, use the `-y` or `--yes` flag:
>
> ```bash
> rye run migrations downgrade -y
> ```

---

##### Show Current Revision

Displays the current migration revision applied in the database:

```bash
rye run migrations current
```

---

##### Show Migration History

Lists the full migration history with applied revisions and their order:

```bash
rye run migrations history
```

---

If you want to automate migrations in your deployment or CI/CD pipeline, it’s recommended to use the `-y` flag to avoid manual confirmation and ensure smooth, non-interactive execution.

---

## 🗂️ Project Structure
This project follows a clean and modular architecture to keep code organized and maintainable. Below is an overview of 
the main folders and files:
```text
./
├── LICENSE                   # Project license
├── README.md                 # Project overview and docs
├── deploy/                   # Deployment configs
│   ├── Dockerfile            # Docker image build file
│   └── docker-compose.yml    # Docker compose for local/dev
├── pyproject.toml            # Python project config and dependencies
├── requirements.lock         # Locked production dependencies
├── requirements-dev.lock     # Locked dev dependencies
└── src/
    └── app/                  # Main application code
        ├── main.py           # App entry point
        ├── asgi.py           # ASGI app instance for async serving
        ├── api/              # API layer (REST endpoints, handlers, schemas)
        │   └── rest/
        │       └── v1/       # API versioning, e.g. conversations endpoints
        │   └── tasks/        # Scheduled tasks
        ├── configs/          # Application configuration modules
        ├── container/        # Dependency injection container & wrappers
        ├── exceptions/       # Custom exceptions & error handling
        ├── infrastructure/  # DB access, migrations, scheduling, etc.
        │   └── database/
        │       └── migrations/ # Alembic migrations and CLI
        ├── models/           # ORM models / domain entities
        ├── repositories/     # Data access layer (repositories pattern)
        ├── service_layer/    # Business logic and transaction coordination
        └── utils/            # Utility helpers (orm, regex, schemas, timestamps)
```

---

## 🛠️ Development

---

### 🧪 Running Tests
<!-- How to run tests (e.g., pytest) -->

---

## 🛠️ Development

### 🎨 Code Style & Linting

This project uses the following tools to ensure consistent code style and maintain code quality:

* **Ruff** — for formatting and linting Python code with configuration for 120 character line length, 4-space indent, and double quotes.
* **Mypy** — for static type checking with strict mode enabled, including plugins for Pydantic and SQLAlchemy.
* **Bandit** — for security analysis of Python code, configured to skip some known false positives.

You can run these checks individually via Rye scripts or combined:

```bash
rye run lint               # Run ruff linter
rye run typecheck          # Run mypy type checks
rye run security-check     # Run Bandit security scan
rye run check-all          # Run all checks: ruff format & lint, mypy, bandit
```

---

## 🚢 Deployment

Deployment is done using Docker with the provided Dockerfile and docker-compose configuration found in the `deploy` folder.

To build and run the application locally:

```bash
docker-compose -f deploy/docker-compose.yml up --build
```

This will build the image and start the service with environment variables as configured.

For production deployments, customize environment variables and possibly use your own orchestration tooling based on the Docker image and compose files provided.

---

## 🛠️ Troubleshooting

Common issues and resolutions:

* **Database connection errors:**
  Ensure your `MIGRATIONS_URL_DATABASE` environment variable is correctly set to the PostgreSQL URL before running migrations or starting the app.

* **Migration conflicts or errors:**
  Use the migration CLI (`rye run migrations`) to check the current revision or history and verify migration state.

* **Linting or type check failures:**
  Run `rye run check-all` to find formatting, linting, type errors, and fix formatting automatically with `ruff`.

* **Dependency issues:**
  Use Rye for dependency management; run `rye sync` to install/update dependencies according to `pyproject.toml`.

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 🙏 Acknowledgements

This project was inspired by and builds upon multiple open-source Python and FastAPI templates, leveraging:

* FastAPI framework for building APIs
* SQLAlchemy for ORM and database management
* Alembic for database migrations
* Rye for modern Python dependency and script management
* Community tools for linting, type checking, and security auditing

Thanks to all maintainers and contributors of these upstream projects.

---