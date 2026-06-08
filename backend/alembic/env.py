from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# ---------------------------------------------------------
# Load environment variables from .env
# ---------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# ---------------------------------------------------------
# Ensure backend root is added to PYTHONPATH
# ---------------------------------------------------------
sys.path.insert(0, BASE_DIR)

# Import Base metadata AFTER PYTHONPATH fix
from app.db.base import Base

# Alembic Config object
config = context.config

# ---------------------------------------------------------
# Inject DATABASE_URL from environment (with % escaping)
# ---------------------------------------------------------
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Alembic uses ConfigParser → % must be escaped as %%
    safe_url = database_url.replace("%", "%%")
    config.set_main_option("sqlalchemy.url", safe_url)

# ---------------------------------------------------------
# Logging config
# ---------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------
# Alembic needs metadata from your models
# ---------------------------------------------------------
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
