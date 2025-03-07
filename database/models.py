import sqlite3
from config.settings import DATABASE_URL


def create_tables():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        firstname TEXT,
        lastname TEXT,
        telegram_id INTEGER UNIQUE,
        registration_date TEXT
    )
    """)

    # Создание таблицы групп
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        name TEXT
    )
    """)

    # Создание таблицы администраторов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE
    )
    """)

    # Создание таблицы для Вип пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vip_panel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        name TEXT
    )""")

    conn.commit()
    conn.close()
