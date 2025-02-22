keyboard_main_admin = [
    ("Получить информацию о товаре", "download_picture_data"),
    ("Скачать видео с товара", "download_video_data"),
    ("VIP 👑", "vip_data"),
    ("Админ панель", "admin_data"),
]

keyboard_main = [
    ("Получить информацию о товаре", "download_picture_data"),
    ("Скачать видео с товара", "download_video_data"),
    ("VIP 👑", "vip_data"),
]



admin_panel_keyboard = [
    ("🧑‍💼Рассылка", "broadcast_message"),
    ("👤Добавить нового админа", "new_admin_data"),
    ("❌Удалить админа", "remove_admin_list_data"),
    ("📈Добавить новую группу для подписки", "add_new_group_username_data"),
    ("📉Удалить группу", "delete_group_data"),
    ("📁Список групп", "list_group_data"),
    ('👤Новый пользователь Vip Panel', "add_new_user_vip_panel"),
    ('❌Удалить пользователя Vip Panel', "delete_user_with_vip_panel"),
    ("🧑Список администрации", "database_list_admin_data"),
    ("🧑‍💼Получить ID пользователя", "get_player_id"),
    ("🔙Назад", "back_data"),
]

back_keyboard = [
    ("🔙Назад", "back_data2"),
]






more_keyboard = [
    ("Другой товар 🔄", "more_download_picture"),
]

more_keyboard_video = [
    ("Другой товар 🔄", "more_download_video"),
]










show_vip_keyboard = [
    ('Парсер товаров 🗂️', 'pars_all_product'),
    ("Парсер кэшбека 💸", "feedback_cashback_data"),
    ("Парсер выгодного кэшбека 💸", "feedback_cashback_data_100"),
]


# Клавиатура для парсинга всех товаров по запросу
more_xlsx_all_product_keyboard = [
    ('Другой запрос 🔄', 'more_all_product_data')
]


# Клавиатура для парсинга всех товаров по запросу с кешбеком
more_xlsx_product_keyboard = [
    ("Другой запрос 🔄", "more_new_xlsx_ordinary_product_data")
]


more_xlsx_super_product_keyboard = [
    ("Другой запрос 🔄", "more_new_xlsx_super_product_data")
]

