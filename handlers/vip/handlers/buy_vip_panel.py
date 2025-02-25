from aiogram import Router, F
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery

from config.settings import PAYMENT_TOKEN, PRICE
from handlers.admin.functions.admin_help_func import add_new_user_vip_panel
from keyboard.keyboard import show_vip_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


# Обработка кнопки "Купить VIP-панель"
@router.callback_query(F.data == "buy_vip_panel_data")
async def buy_vip(callback: CallbackQuery):
    # Создание инвойса для оплаты
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Покупка доступа к VIP-панель",
        description="Доступ к VIP-функциям бота",
        payload="vip_panel_payment",  # Уникальный идентификатор платежа
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        start_parameter="vip_panel",
        need_name=True,  # Опционально: запросить имя пользователя
        need_phone_number=True,  # Опционально: запросить номер телефона
        prices=PRICE,
    )


# Обработка предварительного запроса оплаты
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Обработка успешной оплаты
# Обработка успешной оплаты
@router.message(F.successful_payment.invoice_payload == "vip_panel_payment")
async def successful_payment_handler(message: Message):
    telegram_id = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    vip_panel_information = {
        'telegram_id': telegram_id,
        'name': fullname
    }

    if add_new_user_vip_panel(vip_panel_information):
        await message.answer(
            "🎉 Поздравляем! Вы успешно купили VIP-панель. Теперь вам доступны все функции!",
            reply_markup=make_row_inline_keyboards(show_vip_keyboard)
        )

        await message.bot.send_message(chat_id=6155920970, text=f'🎉 Добавлен новый пользователь в VIP PANEL'
                                                                f'\n\nINFO:'
                                                                f'\nTELEGRAM_ID: {telegram_id}'
                                                                f'\nUSERNAME: @{username}'
                                                                f'\nFULLNAME: {fullname}')
    else:
        await message.answer('ℹ️ Произошла ошибка! Возможно такой пользователь уже имеется! Деньги не списаны.')
    print(vip_panel_information)


# Обработка других успешных платежей (если payload не совпадает)
@router.message(F.successful_payment.invoice_payload != 'vip_panel_payment')
async def other_payment_handler(message: Message):
    await message.answer('❌ Оплата не прошла! Пожалуйста, попробуйте чуть позже! Деньги не списаны.')

    # Логика для предоставления доступа к VIP-панели
    # Например, сохранить статус пользователя в базе данных
