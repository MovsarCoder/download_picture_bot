import re
import requests
import validators


def get_product_info(url):
    try:
        item_id = int(get_item_id(url))
        print(f"Извлеченный item_id: {item_id}")
        response = requests.get(f"https://card.wb.ru/cards/v4/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}")

        data = response.json()
        print(response.url)

        if not data.get("products"):
            print("Нет данных о товаре.")
            return False

        product = data["products"][0]
        name = product.get("name")
        brand = product.get("brand")
        rating_goods = product.get('reviewRating')
        pics = product.get('pics')
        feedbacks = product.get('feedbacks')

        # Ищем ПЕРВУЮ цену в первом же размере, где она есть
        old_price = None
        for size in product.get("sizes", []):
            if size.get("price") and size["price"].get("product"):
                old_price = size["price"]["product"] / 100  # Переводим в рубли
                break  # Нашли первую цену — выходим

        if old_price is None:
            print("Цена не найдена в товаре")
            return False

        # Расчет скидки (3%) и цены со скидкой
        discount = old_price * 0.0215
        price_with_discount = old_price - discount

        # print(name, brand, old_price, price_with_discount, rating_goods, pics, feedbacks)

        # Определяем корзину (basket) для загрузки изображений
        _short_id = item_id // 100000
        if 0 <= _short_id <= 143:
            basket = '01'
        elif 144 <= _short_id <= 287:
            basket = '02'
        elif 288 <= _short_id <= 431:
            basket = '03'
        elif 432 <= _short_id <= 719:
            basket = '04'
        elif 720 <= _short_id <= 1007:
            basket = '05'
        elif 1008 <= _short_id <= 1061:
            basket = '06'
        elif 1062 <= _short_id <= 1115:
            basket = '07'
        elif 1116 <= _short_id <= 1169:
            basket = '08'
        elif 1170 <= _short_id <= 1313:
            basket = '09'
        elif 1314 <= _short_id <= 1601:
            basket = '10'
        elif 1602 <= _short_id <= 1655:
            basket = '11'
        elif 1656 <= _short_id <= 1919:
            basket = '12'
        elif 1920 <= _short_id <= 2045:
            basket = '13'
        elif 2046 <= _short_id <= 2189:
            basket = '14'
        elif 2190 <= _short_id <= 2405:
            basket = '15'
        else:
            basket = '16'

        # Получаем описание товара
        response2 = requests.get(f'https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{item_id // 1000}/{item_id}/info/ru/card.json')
        result = response2.json().get('description')

        # Проверяем доступность изображений
        url2 = f"https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{item_id // 1000}/{item_id}/images/big/1.webp"
        status_code = requests.get(url=url2).status_code

        if status_code == 200:
            link_str = ''.join([f'https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{item_id // 1000}/{item_id}/images/big/{i}.webp\n'
                                for i in range(1, min(10, pics) + 1)])
        else:
            print('Статус код равен: ', status_code)
            return False

        return name, old_price, price_with_discount, brand, item_id, rating_goods, link_str, feedbacks, result

    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def get_item_id(url):
    if validators.url(url):
        regex = "(?<=catalog/).+(?=/detail)"
        match = re.search(regex, url)
        if match:
            return match[0]
    else:
        return url

    raise ValueError("Не удалось извлечь item_id из URL")
