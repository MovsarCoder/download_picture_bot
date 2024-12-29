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