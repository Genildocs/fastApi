from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os
from fruitableApi.database import Base
from fruitableApi import models
# Importe sua Base de models aqui

# Configuração de logging
config = context.config
fileConfig(config.config_file_name)

# Adiciona o URL do banco de dados manualmente se não estiver no alembic.ini
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", os.getenv("SQLALCHEMY_DATABASE_URL"))

# Conectar a base de dados
target_metadata = models.Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
