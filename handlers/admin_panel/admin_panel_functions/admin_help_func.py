import json

admin_list = '../database/admin_list.txt'
player_data = '../database/players_list_db.txt'


def get_anonim(id):
    try:
        with open(f'{player_data}', 'r', encoding='utf-8') as file:
            # Читаем все строки и убираем пробелы
            data_id = {line.strip() for line in file if line.strip()}  # Используем множество
        return str(id) in data_id
    except FileNotFoundError:
        print(f"Файл {player_data} не найден.")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def write_user_id(id_player, username, lastname):
    with open(f'{player_data}', 'a', encoding='utf-8') as file:
        file.write(f'\n{id_player}\n')
        file.write(f'Username: {username}, Lastname: {lastname}, ID: {id_player}')


def add_new_admin_db(add_admin_id):
    with open(f'{admin_list}', 'r', encoding='utf-8') as file:
        read_file = file.read()
        split_file = read_file.split('\n')
        if add_admin_id not in split_file:
            with open(f'{admin_list}', 'a', encoding='utf-8') as file2:
                file2.write(f'\n{add_admin_id}')
                return True

        elif add_admin_id in split_file:
            print('Такой пользователь уже существует!')
            return False

        else:
            # print('Возможно пользователь уже существует или введены не корректные данные.')
            print('Ошибка! 5534-235')
            return False


def remove_admin_from_db(admin_id):
    try:
        with open(f'{admin_list}', 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]

        if str(admin_id) in lines:
            lines.remove(str(admin_id))
            with open(f'{admin_list}', 'w', encoding='utf-8') as file:
                file.write('\n'.join(lines))
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"Файл '{admin_list}' не найден.")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def checked_admin_list():
    with open(f'{admin_list}', 'r', encoding='utf-8') as file2:
        file_read = file2.readlines()
        file_split = [int(line.strip()) for line in file_read if line.strip()]

        return file_split


def writer_group_to_json(data, filename='../database/groups.json'):
    try:
        # Читаем существующие данные
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Проверяем, существует ли группа с таким же username
    for group in existing_data:
        if group['username'] == data['username']:
            return False  # Возвращаем False, если дубликат найден

    # Добавляем новые данные
    existing_data.append(data)

    # Сохраняем обновленные данные
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)

    return True


def remove_group_from_json(username, filename='../database/groups.json'):
    try:
        # Читаем json файл
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        return False  # Файл не найден, возвращаем False

    # Ищем группу с указанным username
    for group in existing_data:
        if group['username'] == username:
            existing_data.remove(group)  # Удаляем группу
            # Сохраняем обновленные данные
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=4)
            return True  # Возвращаем True, если группа была успешно удалена

    return False  # Возвращаем False, если группа с таким username не найдена


def load_from_json(filename='../database/groups.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# def checked_groups_db():
#     with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#         file_read = file.read()
#         file_split = file_read.split('\n')
#
#         return file_split
#
#
# def add_group_db(group_name):
#     with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#         file_read = file.read()
#         file_split = file_read.split('\n')
#         if group_name not in file_split:
#             with open(f'{database_groups_file}', 'a', encoding='utf-8') as file2:
#                 file2.write(f'\n{group_name}')
#                 return True
#
#         elif group_name in file_split:
#             return False
#
#         else:
#             print('Ошибка 77356-211')
#             return False
#
#
# def remove_group_db(group_name):
#     try:
#         with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#             lines = [line.strip() for line in file.readlines()]
#
#         if group_name in lines:
#             lines.remove(group_name)
#             with open(f'{database_groups_file}', 'w', encoding='utf-8') as file:
#                 file.write('\n'.join(lines))
#             return True
#         else:
#             return False
#     except FileNotFoundError:
#         print(f"Файл '{database_groups_file}' не найден.")
#         return False
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#         return False
#
#
# def read_group_file():
#     try:
#         keyboard = []
#         with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#             file_read = file.read()
#             file_split = file_read.split('\n')
#             for i in file_split:
#                 keyboard.append([InlineKeyboardButton(text=f'{i}', url=f'https://t.me/{i}')])
#
#             keyboard_list = InlineKeyboardMarkup(inline_keyboard=keyboard)
#             return keyboard_list
#
#     except Exception as e:
#         print(f'Ошибка типа: {e} - (9990-0001)')
