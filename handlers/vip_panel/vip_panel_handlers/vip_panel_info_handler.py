from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboard.keyboard import show_vip_keyboard, back_vip_keyboard
from keyboard.keyboard_builder import make_row_inline_keyboards

router = Router()


# Выводит всю информацию про Рубли за отзывы
@router.callback_query(F.data == 'show_vip_data_info')
async def show_vip_data_info_func(callback: CallbackQuery):
    description = """
            1) Не так давно на маркетплейсе Wildberries стало возможным зарабатывать рубли за оставленный отзыв. И это правильное решение, особенно в наше время, когда интернет-шопинг стал неотъемлемой частью повседневной жизни. Пользователи достаточно часто ориентируются именно на отзывы других покупателей перед тем, как сделать покупку. Мнения и рекомендации людей, уже опробовавших товар, могут существенно повлиять на решение о покупке, особенно в случаях, когда товар или продавец на площадке новые.\n
            2) Именно поэтому маркетплейс Wildberries предложил новую возможность для своих пользователей — зарабатывать рубли за оставленные отзывы. Теперь ваш труд и время, затраченные на написание подробного и информативного отзыва, будут вознаграждены. Чтобы найти эти товары, можно воспользоваться специальным фильтром в меню поиска. Этот фильтр поможет найти продукцию, за отзывы на которую предусмотрена оплата.\n
            3) Фильтр так и называется: «Рубли за отзыв». Стоит отметить, что далеко не любой категории присутствуют подобные товары. Для того чтобы воспользоваться этой возможностью, нужно оставить отзыв на определенные товары. Wildberries регулярно выбирает товары, за отзывы на которые пользователи получат вознаграждение.\n
            4) Пример аналогичного фильтра «Рубли за отзыв» в мобильном приложении. Стоит отметить, что за ряд товаров предлагается сумма возврата за отзыв больше, чем стоимость самого товара. То есть можно получать дополнительную прибыль в случаях, когда был оформлен товар, условно, за 350 рублей, а получено за отзыв — 600 рублей.\n
            ВАЖНО!!!!!\n
            5) Оставляя отзыв, важно не просто написать пару фраз о товаре, а поделиться своими впечатлениями, опытом использования, плюсами и минусами. Также потребуется сделать фотографии приобретенного товара, чтобы подтвердить свою действительную покупку. Обратите внимание, ситуации с заказами бывают разные и стоит подробно описывать, чтобы следующий покупатель смог воспользоваться вашим опытом. После того как ваш отзыв будет опубликован и проверен администрацией Wildberries, на вашем аккаунте будут начислены рубли в соответствии с условиями программы. Это не только позволяет пользователям зарабатывать дополнительные средства, но и помогает продавцам получать честные и объективные отзывы на свой товар.\n
            6) Полученные средства можно потратить при оформлении следующей покупки на Wildberries, что делает это предложение еще более привлекательным для пользователей. Теперь каждый отзыв может стать не только полезным для других покупателей, но и приятным источником дохода для автора. Таким образом, новая функция маркетплейса Wildberries позволяет справедливо оценивать труды пользователей за полезные отзывы и создает благоприятную среду для обмена мнениями и опытом среди покупателей. Попробуйте себя в качестве автора отзывов и оцените, как ваше мнение может быть ценно и полезно. Ведь теперь и ваши отзывы могут быть оценены по достоинству и принести вам не только удовлетворение, но и реальные денежные средства.\n
            
            
            ВАЖНО!!!\n
            Пользовательское соглашение гласит. Если продавец не скинет вам обещанные деньги за отзыв, владелец бота и люди делегирующие бота не несут никакой ответственности за это. Некоторые продавы могут поставить функция "Рубли за отзыв" На свой товар не показывая этого на карточке. Но программа считывает все что находит под капотом. И в файле может оказаться товар без кешбека под видом кешбека в целях заманить вас в ловушку!\n
            Также некоторые продавцы ставят эту функцию и не отдают деньги за отзыв. В таком случае следует просмотреть отзывы с товара и если все пишут про товар положительно - Заказывать товар.\n
            Вам могут также не заплатить за отзыв, важно прочитать эти правила и условия и понять их, дабы не попадать в такие ситуации.

            """
    await callback.answer('')

    await callback.message.edit_text(f'Все важные правила которые надо запомнить при использования функции Кешбека!\n{description}', reply_markup=make_row_inline_keyboards(back_vip_keyboard))





















@router.callback_query(F.data == 'back_show_vip_data')
async def back_vip_keyboard_func(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите ваше действие: ', reply_markup=make_row_inline_keyboards(show_vip_keyboard))