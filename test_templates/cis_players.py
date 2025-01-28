import sqlite3

database_url = f'../database/database.db'


def create_table():
    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    # Создание базы данных для сохранения всех пользователей
    cursor.execute("""CREATE TABLE IF NOT EXISTS users
    (
    id INTEGER PRIMARY KEY, 
    fullname TEXT,
    firstname TEXT,
    lastname TEXT,
    telegram_id INTEGER,
    registration_date TEXT 
    )
    """)

    # Создание базы данных для сохранения групп на которые нужн подписаться
    cursor.execute("""CREATE TABLE IF NOT EXISTS groups_list
    (
    id INTEGER PRIMARY KEY, 
    username TEXT,
    name TEXT
    )
    """)

    # Создание базы данных для хранения админов
    cursor.execute("""CREATE TABLE IF NOT EXISTS admin_list
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE
        )
        """)

    conn.commit()
    conn.close()



# Взять человека из базы данных
def get_user_with_database(telegram_id):
    conn = sqlite3.connect(database_url)
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*) FROM users WHERE telegram_id = ?
    """, (telegram_id,))

    tasks = cur.fetchone()[0]
    print(tasks)
    conn.close()

    return tasks > 0



"""

    conn = sqlite3.connect(database_url)
    cursor = conn.cursor()

    conn.commit()
    conn.close()


Добавление человека в базу данных 
append_database_users('Мовсар Тутуев', 'Мовсар', 'Тутуев', 1, '23467')





"""