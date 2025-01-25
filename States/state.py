from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    new_admin = State()
    remove_admin = State()
    add_new_group_name = State()
    add_new_group_username = State()
    delete_group = State()
    get_player_id = State()


class Wildberries(StatesGroup):
    download_video = State()
    download_picture = State()


class NewsLetter(StatesGroup):
    text = State()

class WildberriesCashback(StatesGroup):
    get_name_product = State() # Обычный кешбэк
    get_name_super_cashback_product = State()
    get_name_all_product = State()
