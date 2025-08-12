"""
!!!!!!!!!!!!!!!!!!!!!!!

ЗАПУСКАТЬ ИЗ ПАПКИ `backend`
python setup\migrations\setup_alembic.py


ИСПОЛЬЗОВАТЬ !ТОЛЬКО! ПРИ ИНИЦИАЛИЗАЦИИ НОВОГО ПРОЕКТА (КОГДЕ НЕТ БАЗЫ)

!!!!!!!!!!!!!!!!!!!!!!!
"""
import os
import shutil
import subprocess

ALEMBIC_DIR = "alembic"
ALEMBIC_INI = "alembic.ini"
SETUP_DIR = "setup/migrations"


def run(cmd):
    print(f">>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main():
    # Удаляем папку alembic, если есть
    if os.path.exists(ALEMBIC_DIR):
        print(f"Удаляю папку {ALEMBIC_DIR}...")
        shutil.rmtree(ALEMBIC_DIR)

    # Инициализируем alembic
    run(["alembic", "init", ALEMBIC_DIR])

    # Копируем эталонный alembic.ini в корень backend/
    src_ini = os.path.join(SETUP_DIR, "alembic.ini")
    dst_ini = ALEMBIC_INI
    print(f"Копирую {src_ini} -> {dst_ini}")
    shutil.copyfile(src_ini, dst_ini)

    # Копируем эталонный env.py в alembic/
    src_env = os.path.join(SETUP_DIR, "env.py")
    dst_env = os.path.join(ALEMBIC_DIR, "env.py")
    print(f"Копирую {src_env} -> {dst_env}")
    shutil.copyfile(src_env, dst_env)

    # Делаем ревизию с автогенерацией
    run(["alembic", "revision", "--autogenerate", "-m", "init"])

    # Применяем миграции
    run(["alembic", "upgrade", "head"])

    print("Alembic успешно настроен и миграции применены.")


if __name__ == "__main__":
    main()
