import sqlite3
from datetime import datetime
from config.settings import DATABASE_URL


def write_user(username, fullname, firstname, lastname, telegram_id):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = (username, fullname, firstname, lastname, telegram_id, registration_date)

    try:
        cursor.execute("""
        INSERT INTO users (username, fullname, firstname, lastname, telegram_id, registration_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
    except sqlite3.IntegrityError:
        return
    finally:
        conn.close()


def user_exists(telegram_id):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists


def select_to_table(telegram_id: int):
    conn = sqlite3.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM users WHERE telegram_id = ?""", (telegram_id,))
    get_info = cur.fetchone()
    conn.close()
    return_info = {
        "id": get_info[0],
        "username": get_info[1],
        "fullname": get_info[2],
        "firstname": get_info[3],
        "lastname": get_info[4],
        "telegram_id": get_info[5],
        "sign_up_people": get_info[6],
    }
    return return_info


def add_admin(telegram_id):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO admin_list (telegram_id) VALUES (?)", (telegram_id,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Администратор с telegram_id {telegram_id} уже существует.")
        return False
    finally:
        conn.close()


def remove_admin(telegram_id):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM admin_list WHERE telegram_id = ?", (telegram_id,))
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        print(f"Администратор с telegram_id {telegram_id} не существует.")
        return False

    finally:
        conn.close()


def get_admin_list():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT telegram_id FROM admin_list")
    admin_list = [row[0] for row in cursor.fetchall()]

    conn.close()
    return admin_list


def add_group(group_data):
    conn = sqlite3.connect(DATABASE_URL)
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
    conn = sqlite3.connect(DATABASE_URL)
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
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT username, name FROM groups_list")
    groups = [{"username": row[0], "name": row[1]} for row in cursor.fetchall()]

    conn.close()
    return groups


def get_player_vip_panel(data):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM vip_panel WHERE telegram_id = ?
        """, (data['telegram_id'],))

        result = cursor.fetchone()[0]  # Получаем количество записей
        conn.close()

        return result > 0  # Возвращаем True, если пользователь уже существует
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False


def add_new_user_vip_panel(data):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Проверяем, существует ли пользователь
        if get_player_vip_panel(data):
            conn.close()
            return False

        # Добавляем пользователя
        cursor.execute("""
            INSERT INTO vip_panel (telegram_id, name) VALUES (?, ?)
        """, (data['telegram_id'], data['name']))

        conn.commit()
        conn.close()
        return True  # Возвращаем True, если пользователь успешно добавлен
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False


def delete_users_with_vip_panel_functions(data):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()

    if get_player_vip_panel(data):  # Если человека нет в базе данных
        cursor.execute("""
                DELETE FROM vip_panel WHERE telegram_id = ?
                """, (data['telegram_id'],))

        conn.commit()
        conn.close()
        print('Человек успешно удален!')
        return True


    else:  # Если такого нет в базе данных
        print('Такого пользователя нет в базе данных!')
        return False


def get_chat_id():
    """Функция для получения всех telegram_id пользователей из базы данных SQLite"""

    # Подключаемся к базе данных
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:

        # Выполняем запрос
        cursor.execute("SELECT telegram_id FROM users")

        # Получаем все результаты и преобразуем в список чисел
        results = cursor.fetchall()
        return [row[0] for row in results]

    except sqlite3.Error as e:
        print(f"Ошибка при получении chat_id: {e}")
        return []

    finally:
        conn.close()
