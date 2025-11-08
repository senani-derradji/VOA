from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os, sys

config = context.config

sys.path.append(os.path.join(os.path.dirname(__file__)))
from app.extentions.database import Base
from app.core.config import settings
# Load values securely from encrypted settings
use_sqlite = settings.get("USE_SQLITE", "false").lower() == "true"
sqlite_path = settings.get("DB_PATH", "./VOA.db")

db_user = settings.get("DB_USER", "postgres")
db_pass = settings.get("DB_PASSWORD", "postgres")
db_host = settings.get("DB_HOST", "database")
db_port = settings.get("DB_PORT", "5432")
db_name = settings.get("DB_NAME", "VOA")

if use_sqlite:
    database_url = f"sqlite:///{sqlite_path}"
else:
    database_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

config.set_main_option("sqlalchemy.url", database_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
