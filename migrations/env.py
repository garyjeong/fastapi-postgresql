import os
import re
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool
import sqlalchemy as sa

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.configs.database import AppEnv, Base, create_engine_with_tunnel
from src.models.base import *
from src.models.template_1.users import Users
from src.models.template_2.vehicles import Vehicles
from src.models.template_3.jobs import Jobs


env = os.getenv("ENV", AppEnv.LOCAL)
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url(env: AppEnv = AppEnv.LOCAL):
    return create_engine_with_tunnel(env=env).url


def run_migrations_offline() -> None:
    url = get_url(env=env)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(name=config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url(env=env)

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS template_1"))
        connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS template_2"))
        connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS template_3"))
        connection.commit()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
            version_table_schema="public",
            include_object=lambda obj, name, type_, reflected, compare_to: True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
