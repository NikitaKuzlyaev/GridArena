import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, project_root)

from backend.configuration.settings import settings

# Строка подключения к целевой базе (та, что должна быть создана)
DATABASE_URL = settings.MAIN_SYNC_DATABASE_URI


def create_database_if_not_exists(database_url: str):
    parsed_url = urlparse(database_url)

    # Извлекаем параметры подключения
    dbname = parsed_url.path.lstrip('/')
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port or 5432

    # Подключаемся к postgres (служебная база) для проверки/создания базы
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # todo: check others

    cur = conn.cursor()

    # Проверяем существует ли база
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (dbname,))
    exists = cur.fetchone()

    if exists:
        print(f"Database '{dbname}' already exists.")
    else:
        # Создаем базу
        try:
            cur.execute(f'CREATE DATABASE "{dbname}"')
            print(f"Database '{dbname}' created successfully.")
        except Exception as e:
            print(f"Failed to create database '{dbname}': {e}", file=sys.stderr)
            sys.exit(1)

    cur.close()
    conn.close()


if __name__ == "__main__":
    create_database_if_not_exists(DATABASE_URL)
