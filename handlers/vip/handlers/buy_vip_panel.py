from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery

from States.state import BuyVipPanel
from config.settings import PAYMENT_DETAILS, VIP_SUBSCRIPTION_PRICE, SENDING_RECEIPT, ADMIN

from config.settings import PAYMENT_TOKEN, PRICE
from database.crud import add_new_user_vip_panel
from keyboard.keyboard import show_vip_keyboard, accept_or_cancel_cheque
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()

# ##########################################################################
# # ---------- Покупка "VIP-панели" с помощью нажатия кнопки ---------- ####
# ##########################################################################



# # Обработка кнопки "Купить VIP-панель"
# @router.callback_query(F.data == "buy_vip_panel_data")
# async def buy_vip(callback: CallbackQuery):
#     # Создание инвойса для оплаты
#     await callback.bot.send_invoice(
#         chat_id=callback.from_user.id,
#         title="Покупка доступа к VIP-панель",
#         description="Доступ к VIP-функциям бота",
#         payload="vip_panel_payment",  # Уникальный идентификатор платежа
#         provider_token=PAYMENT_TOKEN,
#         currency="RUB",
#         start_parameter="vip_panel",
#         need_name=True,  # Опционально: запросить имя пользователя
#         need_phone_number=True,  # Опционально: запросить номер телефона
#         prices=PRICE,
#     )
#
#
# # Обработка предварительного запроса оплаты
# @router.pre_checkout_query()
# async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
#     await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#
#
# # Обработка успешной оплаты
# # Обработка успешной оплаты
# @router.message(F.successful_payment.invoice_payload == "vip_panel_payment")
# async def successful_payment_handler(message: Message):
#     telegram_id = message.from_user.id
#     fullname = message.from_user.full_name
#     username = message.from_user.username
#
#     vip_panel_information = {
#         'telegram_id': telegram_id,
#         'name': fullname
#     }
#
#     if add_new_user_vip_panel(vip_panel_information):
#         await message.answer(
#             "🎉 Поздравляем! Вы успешно купили VIP-панель. Теперь вам доступны все функции!",
#             reply_markup=make_row_inline_keyboards(show_vip_keyboard)
#         )
#
#         await message.bot.send_message(chat_id=6155920970, text=f'🎉 Добавлен новый пользователь в VIP PANEL'
#                                                                 f'\n\nINFO:'
#                                                                 f'\nTELEGRAM_ID: {telegram_id}'
#                                                                 f'\nUSERNAME: @{username}'
#                                                                 f'\nFULLNAME: {fullname}')
#     else:
#         await message.answer('ℹ️ Произошла ошибка! Возможно такой пользователь уже имеется! Деньги не списаны.')
#     print(vip_panel_information)
#
#
# # Обработка других успешных платежей (если payload не совпадает)
# @router.message(F.successful_payment.invoice_payload != 'vip_panel_payment')
# async def other_payment_handler(message: Message):
#     await message.answer('❌ Оплата не прошла! Пожалуйста, попробуйте чуть позже! Деньги не списаны.')
#
#     # Логика для предоставления доступа к VIP-панели
#     # Например, сохранить статус пользователя в базе данных





# ##########################################################################
# # ---------- Покупка "VIP-панели" с помощью нажатия кнопки ---------- ####
# ##########################################################################

ADMIN = ADMIN
SENDING_RECEIPT = SENDING_RECEIPT
PAYMENT_DETAILS = PAYMENT_DETAILS
VIP_SUBSCRIPTION_PRICE = VIP_SUBSCRIPTION_PRICE


# Выводится сообщение с реквизитами для покупки VIP-панели
@router.callback_query(F.data == 'buy_vip_panel_data')
async def buy_vip_panel(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(f"""
    💳 Для оплаты <b>VIP</b> подписки, пожалуйста, переведите сумму <b>{VIP_SUBSCRIPTION_PRICE}</b> на следующие реквизиты:
    
    📌 [<b>Реквизиты для оплаты</b>] - {PAYMENT_DETAILS} (Сбербанк Онлайн)
    
    📸 После оплаты, отправьте скриншот чека в этот чат для проверки. 
    
    ✅ Как только оплата будет подтверждена, вы будете добавлены в <b>VIP Panel</b>.
    
    ⏳ [<b>Обратите внимание</b>] - подписка действует <b>всего лишь на одну неделю</b>. По истечении этого срока доступ к VIP Panel будет автоматически прекращен. Если вы хотите продлить подписку, пожалуйста, повторите оплату.
    """)

    await state.set_state(BuyVipPanel.get_photo)


# Идет проверка на отправленный чек
@router.message(BuyVipPanel.get_photo, F.content_type.in_({"text", "photo", "video", "document"}))
async def send_receipt(message: Message, state: FSMContext):
    user_info = f"""
    TELEGRAM_ID - {message.from_user.id}\n
    USERNAME - @{message.from_user.username or None}\n
    FULLNAME - {message.from_user.full_name}\n
    FIRST_NAME - {message.from_user.first_name or None}\n
    LAST_NAME - {message.from_user.last_name or None}\n
    Время отправки чека: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n
    Подпись сообщения - {message.caption if message.caption else None}
    """


    try:
        # Определяем тип контента
        if message.text:
            await message.answer(f"❌Не удалось отправить чек для проверки оплаты!\n\n🛠️Связь с тех. оператором: {ADMIN}")

        elif message.photo:
            # Рассылка фото
            await message.bot.send_photo(
                chat_id=int(SENDING_RECEIPT),
                photo=message.photo[-1].file_id,
                caption=user_info,
                reply_markup=make_row_inline_keyboards(accept_or_cancel_cheque)
            )
        elif message.video:
            # Рассылка видео
            await message.bot.send_video(
                chat_id=int(SENDING_RECEIPT),
                video=message.video.file_id,
                caption=user_info,
                reply_markup=make_row_inline_keyboards(accept_or_cancel_cheque)
            )
        elif message.document:
            # Рассылка документа
            await message.bot.send_document(
                chat_id=int(SENDING_RECEIPT),
                document=message.document.file_id,
                caption=user_info,
                reply_markup=make_row_inline_keyboards(accept_or_cancel_cheque)
            )

        else:
            await message.answer('Ошибка неизвестного типа! (234567-4345)')


        # Если чек успешно отправлен администратору, отправляется это сообщение
        await message.answer(f"""
📨 <b>Ваш чек успешно получен!</b> 
Спасибо за отправку! Мы уже начали проверку вашего платежа.  

⏳ Пожалуйста, подождите немного, пока мы подтвердим оплату. Обычно это занимает несколько минут.  

✅ Как только оплата будет подтверждена, вы получите уведомление и будете добавлены в <b>VIP Panel</b>!  

🙏 Благодарим за ваше терпение! Если у вас есть вопросы, не стесняйтесь обращаться.  

🛠️Связь с тех. оператором: {ADMIN}
        """)


        # Если администратор подтвердил оплату, пользователь добавляется в базу данных и выводится это сообщение.
        @router.callback_query(F.data == 'accept_cheque')
        async def accept_cheque_function(callback: CallbackQuery):
            await message.answer(f"""
🎉 <b>Оплата подтверждена!</b>
Ваш чек успешно проверен, и оплата подтверждена.  

✅ Теперь вы добавлены в <b>VIP Panel</b>!  
Наслаждайтесь всеми преимуществами VIP-статуса.  

🙏 Спасибо за вашу оплату! Если у вас есть вопросы, не стесняйтесь обращаться.  

🛠️Связь с тех. оператором: {ADMIN}
            """)

            vip_panel_information = {
                'telegram_id': message.from_user.id,
                'name': message.from_user.username,
            }

            if add_new_user_vip_panel(vip_panel_information):
                await callback.message.answer('✅ Пользователь успешно добавлен в базу данных VIP!')
            else:
                await callback.message.answer('❌ Пользователь уже существует в базе данных VIP!')


        # Если администратор отменил оплату, выводится это сообщение и если по программному сбою отменился чек, то можно связаться с администратором.
        @router.callback_query(F.data == 'cancel_cheque')
        async def cancel_cheque_function(callback: CallbackQuery):
            await message.answer(f"""
❌ <b>Оплата не подтверждена</b>
К сожалению, мы не смогли подтвердить ваш платеж.  

Возможные причины:  
- Чек нечеткий или нечитаемый.  
- Оплата не поступила на наш счет.  
- Неверные реквизиты для оплаты.  

📸 Пожалуйста, проверьте данные и отправьте чек еще раз. Если проблема сохраняется, свяжитесь с нами для помощи.  
🛠️Связь с тех. оператором: {ADMIN}

🙏 Спасибо за понимание!  
            """)


            await callback.message.answer('❌ Пользователь не был добавлен в базу данных VIP!')


    except Exception as e:
        await message.answer(f"❌Не удалось отправить чек для проверки оплаты! - {e}\n\n🛠️Связь с тех. оператором: {ADMIN}")

    finally:
        await state.clear()





