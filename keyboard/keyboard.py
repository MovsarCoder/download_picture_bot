from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# keyboard_main_admin = [
#     ("Получить информацию о товаре", "download_picture_data"),
#     ("Скачать видео с товара", "download_video_data"),
#     ("VIP 👑", "vip_data"),
#     ("Админ панель", "admin_data"),
# ]
#
# keyboard_main = [
#     ("Получить информацию о товаре", "download_picture_data"),
#     ("Скачать видео с товара", "download_video_data"),
#     ("VIP 👑", "vip_data"),
# ]

keyboard_main_admin = [
    ("ℹ️ Личная информация"),
    ("🛍️ Информация о товаре"),
    ("📥 Скачать видео"),
    ("💎 VIP-доступ"),
    ("⚙️ Управление ботом"),
]

keyboard_main = [
    ("ℹ️ Личная информация"),
    ("🛍️ Информация о товаре"),
    ("📥 Скачать видео"),
    ("💎 VIP-доступ"),
    ("⚙️ Управление ботом"),
]








admin_panel_keyboard = [
    ("📢 Создать рассылку", "broadcast_message"),
    ("➕ Добавить админа", "new_admin_data"),
    ("➖ Удалить админа", "remove_admin_list_data"),
    ("➕ Добавить группу", "add_new_group_username_data"),
    ("➖ Удалить группу", "delete_group_data"),
    ("📂 Список групп", "list_group_data"),
    ("➕ Добавить VIP", "add_new_user_vip_panel"),
    ("➖ Удалить VIP", "delete_user_with_vip_panel"),
    ("👥 Список админов", "database_list_admin_data"),
    ("🆔 Получить ID", "get_player_id"),
]

back_keyboard = [
    ("🔙Назад", "back_data2"),
]











# Клавиатура для загрузки другого товара (изображение)
more_keyboard = [
    ("🔄 Новый товар", "more_download_picture"),
]

# Клавиатура для загрузки другого товара (видео)
more_keyboard_video = [
    ("🔄 Новый товар", "more_download_video"),
]







# Покупка вип панели
buy_vip_panel_keyboard = [
    ('Купить VIP 💎', 'buy_vip_panel_data')
]




# Клавиатура для VIP-функций
show_vip_keyboard = [
    ('🗂️ Парсер товаров', 'pars_all_product'),  # Парсер всех товаров
    ("💸 Парсер кэшбека", "feedback_cashback_data"),  # Парсер кэшбека
    ("💎 Парсер выгодного кэшбека", "feedback_cashback_data_100"),  # Парсер выгодного кэшбека
]

# Клавиатура для парсинга всех товаров по запросу
more_xlsx_all_product_keyboard = [
    ('🔄 Новый запрос', 'more_all_product_data')  # Новый запрос для парсинга всех товаров
]

# Клавиатура для парсинга всех товаров по запросу с кешбеком
more_xlsx_product_keyboard = [
    ("🔄 Новый запрос", "more_new_xlsx_ordinary_product_data")  # Новый запрос для парсинга товаров с кешбеком
]

# Клавиатура для парсинга всех товаров по запросу с выгодным кешбеком
more_xlsx_super_product_keyboard = [
    ("🔄 Новый запрос", "more_new_xlsx_super_product_data")  # Новый запрос для парсинга товаров с выгодным кешбеком
]

# Клавиатура для подтверждения чека
accept_or_cancel_cheque = [
    ("✅Подтвердить оплату ", "accept_cheque"),
    ("❌Отменить оплату", "cancel_cheque"),
]


def make_pay(user_id, name = None) -> InlineKeyboardMarkup:
    row = [
        [InlineKeyboardButton(text= '✅Подтвердить оплату ', callback_data=f'accept_cheque_{user_id}_{name}')],
        [InlineKeyboardButton(text= '❌Отменить оплату ',callback_data=f'cancel_cheque_{user_id}_{name}')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=row)