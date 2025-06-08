from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext

from keyboard.keyboard import *
from database.crud import *
from keyboard.keyboard_builder import make_row_keyboards

router = Router()


async def handle_subscription_check(message: Message, groups):
    keyboard = []
    not_subscribed_channels = []

    list_admins = get_admin_list()
    if message.from_user.id in list_admins:
        await message.answer('🌟 Добро пожаловать в нашего бота! 🌟 Мы рады, что вы с нами! 😊 \n\nЧтобы узнать больше о возможностях бота и удобных командах, просто нажмите /help. 📚\n\nА пока предлагаем вам воспользоваться нашим функционалом и убедиться, как мы можем сделать вашу жизнь проще и интереснее! 🚀\n\nЕсли возникнут вопросы, не стесняйтесь обращаться — мы всегда готовы помочь! 💬✨',
                             reply_markup=make_row_keyboards(keyboard_main_admin))
        return

    for i in groups:
        member = await message.bot.get_chat_member(chat_id=f'@{i["username"]}', user_id=message.from_user.id)
        if member.status not in ['member', 'creator', 'administrator']:
            keyboard.append([InlineKeyboardButton(text=f'{i["name"]}', url=f'https://t.me/{i["username"]}')])
            not_subscribed_channels.append(i)  # Добавляем неподписанный канал в список

    # Добавляем кнопку проверки подписок только если есть неподписанные каналы
    # if not_subscribed_channels:
    #     keyboard.append([InlineKeyboardButton(text='Проверить подписку', callback_data='check_subscribes')])

    keyboard_subscribe = InlineKeyboardMarkup(inline_keyboard=keyboard)

    if keyboard:  # Если есть каналы для подписки
        await message.answer('Подпишитесь на все каналы, чтобы продолжить пользоваться ботом!',
                             reply_markup=keyboard_subscribe)
    else:
        await message.answer('🌟 Добро пожаловать в нашего бота! 🌟 Мы рады, что вы с нами! 😊 \n\nЧтобы узнать больше о возможностях бота и удобных командах, просто нажмите /help. 📚\n\nА пока предлагаем вам воспользоваться нашим функционалом и убедиться, как мы можем сделать вашу жизнь проще и интереснее! 🚀\n\nЕсли возникнут вопросы, не стесняйтесь обращаться — мы всегда готовы помочь! 💬✨',
                             reply_markup=make_row_keyboards(keyboard_main))


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    groups = load_groups()
    a = user_exists(message.from_user.id)

    if not a:
        write_user(message.from_user.username, message.from_user.full_name, message.from_user.first_name, message.from_user.last_name, message.from_user.id)
        await handle_subscription_check(message, groups)

    else:
        await handle_subscription_check(message, groups)

#
# @router.callback_query(F.data == 'more_stop')
# async def more_send_stop(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     list_admins = get_admin_list()
#     if callback.from_user.id in list_admins:
#         await callback.message.answer('Добро пожаловать в наш бот! Удобную информацию про наш бот вы можете посмотреть по команде /help.\n\nА пока воспользуйтесь нашим функционалом.', reply_markup=make_row_inline_keyboards(keyboard_main_admin))
#     else:
#         await callback.message.answer('Добро пожаловать в наш бот! Удобную информацию про наш бот вы можете посмотреть по команде /help.\n\nА пока воспользуйтесь нашим функционалом.', reply_markup=make_row_inline_keyboards(keyboard_main))
#















# @router.callback_query(F.data == 'check_subscribes')
# async def check_subscribes(callback_query: CallbackQuery):
#     user_id = callback_query.from_user.id
#     not_subscribed_channels = []
#     groups = load_from_json()
#     try:
#         for i in groups:
#             member = await callback_query.bot.get_chat_member(chat_id=f'@{i["username"]}', user_id=user_id)
#             if member.status not in ['member', 'creator', 'administrator']:
#                 not_subscribed_channels.append(i["username"])
#
#         if not_subscribed_channels:
#             # Если есть неподписанные каналы, отправляем сообщение
#             keyboard = [[InlineKeyboardButton(text=f'{channel}', url=f'https://t.me/{channel}') for channel in not_subscribed_channels]]
#             # keyboard.append([InlineKeyboardButton(text='Проверить подписку', callback_data='check_subscribes')])
#             keyboard_subscribe = InlineKeyboardMarkup(inline_keyboard=keyboard)
#
#             await callback_query.message.answer('Вы не подписаны на следующие каналы ;', reply_markup=keyboard_subscribe)
#         else:
#             await callback_query.message.answer('Выберите функцию', reply_markup=keyboard_main)
#
#     except Exception as e:
#         print(f"Error checking subscriptions: {e}")
#         await callback_query.answer("Произошла ошибка при проверке подписок.")
#
#
#
#
#
