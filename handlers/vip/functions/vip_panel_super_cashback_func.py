import pandas as pd
import requests


async def create_csv(filename):
    # Создаем DataFrame с заголовками
    df = pd.DataFrame(columns=['id', 'name', 'brand', 'feedbacks', 'price', 'feedbackPoints', 'url', 'rating', 'supplier', 'supplierRating', 'entity'])
    df.to_csv(f'{filename}.csv', index=False, sep=',', encoding='utf-8')


async def save_to_csv(product_id, product_name, product_brand, product_feedbacks, product_price, feedback_points, product_url, product_rating, supplier, supplier_rating, entity, filename):
    # Проверяем, существует ли файл
    df = pd.read_csv(f'{filename}.csv')

    # # Проверяем, существует ли уже запись с таким же id
    # if not df[df['id'] == product_id].empty:
    #     print(f"Продукт с id {product_id} уже существует.")
    #     return

    # Добавляем новую строку
    new_row = {
        'id': product_id,
        'name': product_name,
        'brand': product_brand,
        'feedbacks': product_feedbacks,
        'price': product_price,
        'feedbackPoints': feedback_points,
        'url': product_url,
        'rating': product_rating,
        'supplier': supplier,
        'supplierRating': supplier_rating,
        'entity': entity
    }

    # Добавляем новую строку в DataFrame
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Сохраняем DataFrame обратно в CSV файл
    df.to_csv(f'{filename}.csv', index=False, sep=',')
    # print("Файл успешно сохранен.")


async def create_params(page: int, search_item: str):
    return {
        'ab_testid': 'boost_promo_5',
        'appType': '1',
        'curr': 'rub',
        'dest': '-1257786',
        'ffeedbackpoints': '1',
        'hide_dtype': '10',
        'lang': 'ru',
        'page': str(page),
        'query': f'{search_item}',
        'resultset': 'catalog',
        'sort': 'popular',
        'spp': '30',
        'suppressSpellcheck': 'false',
    }


async def fetch_total_results(search_item):
    initial_params = await create_params(1, search_item)
    response = requests.get('https://search.wb.ru/exactmatch/ru/common/v9/search', params=initial_params)

    if response.status_code == 200:
        return response.json()['data']['total']
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return 0


async def main(search_item):
    await create_csv(search_item)  # Создаем Excel файл один раз в начале
    total_results = await fetch_total_results(search_item)
    total_pages = (total_results // 100) + 2

    all_products = []  # Список для хранения всех товаров

    for page in range(1, total_pages):
        print(f'Страница: {page}')

        params = await create_params(page, search_item)
        response = requests.get('https://search.wb.ru/exactmatch/ru/common/v9/search', params=params)

        if response.status_code == 200:
            products = response.json()['data']['products']

            for product in products:
                # Проверяем существование полей sizes и price
                name = product.get('name', 'Неизвестно')
                product_id = product.get('id', 0)
                create_url = f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx'
                try:
                    if "sizes" in product and product["sizes"]:
                        if "price" in product["sizes"][0]:
                            price = product["sizes"][0]["price"]["product"] // 100
                        else:
                            print(f"У продукта {product_id} отсутствует ключ 'price'. Пропускаем.")
                            continue
                    else:
                        print(f"У продукта {product_id} отсутствует массив 'sizes'. Пропускаем.")
                        continue

                    product_feedbacks = product.get('feedbacks', 0)
                    feedback_points = product.get('feedbackPoints', 0)
                    product_brand = product.get('brand', 'Неизвестно')
                    product_rating = product.get('reviewRating', 0)

                    supplier = product.get('supplier', 'Неизвестно')
                    supplier_rating = product.get('supplierRating', 0)
                    entity = product.get('entity', 'Неизвестно')

                    # Проверяем, что feedbackPoints >= price
                    if feedback_points >= price // 2 and feedback_points > (price * 0.25) / 2:
                        # if min(price):
                        # Добавляем товар в список
                        all_products.append({
                            'id': product_id,
                            'name': name,
                            'brand': product_brand,
                            'feedbacks': product_feedbacks,
                            'price': price,
                            'feedbackPoints': feedback_points,
                            'url': create_url,
                            'rating': product_rating,
                            'supplier': supplier,
                            'supplierRating': supplier_rating,
                            'entity': entity
                        })

                except Exception as e:
                    print(f"Ошибка в обработке продукта {product_id}: {e}")
        else:
            print(f"Ошибка при запросе страницы {page}: {response.status_code}")

    # Сортируем товары по цене
    all_products.sort(key=lambda x: x['price'])

    # Сохраняем отсортированные товары в CSV
    for product in all_products:
        await save_to_csv(
            product['id'],
            product['name'],
            product['brand'],
            product['feedbacks'],
            product['price'],
            product['feedbackPoints'],
            product['url'],
            product['rating'],
            product['supplier'],
            product['supplierRating'],
            product['entity'],
            search_item
        )
