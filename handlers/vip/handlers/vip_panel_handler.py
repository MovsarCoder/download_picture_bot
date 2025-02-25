from aiogram import Router, F
from aiogram.types import Message

from config.settings import ADMIN
from handlers.admin.functions.admin_help_func import get_player_vip_panel
from keyboard.keyboard import show_vip_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


@router.message(F.text == '💎 VIP-доступ')
async def show_vip_keyboard_func(message: Message):
    admin = ADMIN
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_info = {
        'telegram_id': user_id,
        'name': user_name
    }

    checked_vip_list = get_player_vip_panel(user_info)
    if checked_vip_list:
        await message.answer('🎉 Добро пожаловать в VIP-панель! 🎉\n\nТеперь у вас есть доступ к эксклюзивным функциям и возможностям! 🌟\n\nВыберите функцию, которую хотите использовать:',
                                      reply_markup=make_row_inline_keyboards(show_vip_keyboard))

    else:
        await message.answer(
            f'⚠️{message.from_user.full_name}({message.from_user.id}) вы не можете получить доступ к Vip Panel данного бота! Так как не являетесь Пользователем!\n\n👀Для покупки подписки Vip напишите мне: {admin}')
