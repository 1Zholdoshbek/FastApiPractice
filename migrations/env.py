from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from logging.config import fileConfig
import asyncio
import sys
import os

# Добавьте путь к вашему проекту в sys.path
sys.path.append(os.getcwd())

# Импортируйте Base и target_metadata из вашего файла с моделями
from models import Base
target_metadata = Base.metadata

# Настройка Alembic
config = context.config
fileConfig(config.config_file_name)

# Асинхронная функция для запуска миграций
async def run_migrations_online():
    # Получите строку подключения из alembic.ini
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

# Синхронная функция для выполнения миграций
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# Запуск асинхронной функции
if context.is_offline_mode():
    raise Exception("Асинхронные миграции не поддерживаются в offline-режиме.")
else:
    asyncio.run(run_migrations_online())