from aiogram.fsm.state import State, StatesGroup


########################################
# ---------- Admin-панель ---------- ###
########################################


class AdminState(StatesGroup):
    new_admin = State()
    remove_admin = State()
    add_new_group_name = State()
    add_new_group_username = State()
    delete_group = State()
    get_player_id = State()


class NewsLetter(StatesGroup):
    text = State()


########################################
# ---------- Wildberries ---------- ####
########################################

class Wildberries(StatesGroup):
    download_video = State()
    download_picture = State()


class WildberriesCashback(StatesGroup):
    get_name_product = State()  # Обычный кешбэк
    get_name_super_cashback_product = State()
    get_name_all_product = State()


##########################################
# ---------- "VIP-панель"  ---------- ####
##########################################


class BuyVipPanel(StatesGroup):
    get_photo = State()
    # b = State()


class AddedVipPanel(StatesGroup):
    get_id = State()
    get_name = State()


class DeleteVipPanel(StatesGroup):
    get_id = State()
