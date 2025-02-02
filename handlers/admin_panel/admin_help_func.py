import sqlite3
from datetime import datetime

database_url = '../database/database.db'

def create_tables():
    conn = sqlite3.connect(database_url)
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

    conn.commit()
    conn.close()

def write_user(fullname, firstname, lastname, telegram_id):
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = (fullname, firstname, lastname, telegram_id, registration_date)

    try:
        cursor.execute("""
        INSERT INTO users (fullname, firstname, lastname, telegram_id, registration_date)
        VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Пользователь с telegram_id {telegram_id} уже существует.")
    finally:
        conn.close()

def user_exists(telegram_id):
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists

def add_admin(telegram_id):
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO admin_list (telegram_id) VALUES (?)", (telegram_id,))
        conn.commit()
        print("Новый администратор добавлен.")
    except sqlite3.IntegrityError:
        print(f"Администратор с telegram_id {telegram_id} уже существует.")
    finally:
        conn.close()

def remove_admin(telegram_id):
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM admin_list WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()

def get_admin_list():
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("SELECT telegram_id FROM admin_list")
    admin_list = [row[0] for row in cursor.fetchall()]

    conn.close()
    return admin_list

def add_group(group_data):
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO groups_list (username, name) VALUES (:username, :name)", group_data)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Группа с username {group_data['username']} уже существует.")
        return False
    finally:
        conn.close()

def remove_group(username):
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM groups_list WHERE username = ?", (username,))
    if cursor.rowcount == 0:
        print(f"Группа с username {username} не найдена.")
        success = False
    else:
        success = True

    conn.commit()
    conn.close()
    return success

def load_groups():
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    cursor.execute("SELECT username, name FROM groups_list")
    groups = [{"username": row[0], "name": row[1]} for row in cursor.fetchall()]

    conn.close()
    return groups
