import importlib
import os
import re
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.configs.database import AppEnv, Base, create_engine_with_tunnel
from src.models.base import *


def import_models():
    models_path = Path(__file__).parent.parent.parent / "src" / "models"

    for path in models_path.rglob("*.py"):
        if path.name == "base.py" or path.name.startswith("_"):
            continue

        relative_path = path.relative_to(Path(__file__).parent.parent)
        module_path = str(relative_path).replace(os.path.sep, ".")[:-3]
        importlib.import_module(module_path)


import_models()

env = os.getenv("ENV", AppEnv.LOCAL)
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url(env: AppEnv = AppEnv.LOCAL):
    return create_engine_with_tunnel(env=env).url


def get_next_version():
    versions_dir = Path(__file__).parent / "versions"
    if not versions_dir.exists():
        versions_dir.mkdir(exist_ok=True)
        return "1.0"

    version_files = [
        f.name for f in versions_dir.glob("v*.py") if f.name != "__init__.py"
    ]

    if not version_files:
        return "1.0"

    version_numbers = []
    for filename in version_files:
        match = re.match(r"v(\d{8})_.*\.py", filename)
        if match:
            version_numbers.append(match.group(1))

    if not version_numbers:
        return "1.0"

    return str(float(max(version_numbers)) + 0.1)


def run_migrations_offline() -> None:
    url = get_url(env=env)
    print(f"FUCK Offline : {url}")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(name=config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url(env=env)
    print(f"FUCK Online : {configuration['sqlalchemy.url']}")
    connectable = engine_from_config(
        configuration=configuration,
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
