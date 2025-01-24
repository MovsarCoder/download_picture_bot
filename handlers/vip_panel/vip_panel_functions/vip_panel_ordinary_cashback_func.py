import pandas as pd
import requests


async def create_csv(filename):
    # Создаем DataFrame с заголовками
    df = pd.DataFrame(columns=['id', 'name', 'price', 'url', 'brand', 'feedbackPoints', 'supplier', 'supplierRating', 'entity'])
    df.to_csv(f'{filename}.csv', index=False, sep=',')


async def save_to_csv(product_id, product_name, product_price, product_url, product_brand, feedback_points, supplier, supplier_rating, entity, filename):
    # Загружаем существующий файл или создаем новый DataFrame
    try:
        df = pd.read_csv(f'{filename}.csv', sep=',')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['id', 'name', 'price', 'url', 'brand', 'feedbackPoints', 'supplier', 'supplierRating', 'entity'])

    # Проверяем, существует ли уже запись с таким же id
    if not df[df['id'] == product_id].empty:
        print(f"Продукт с id {product_id} уже существует.")
        return

    # Добавляем новую строку
    new_row = {
        'id': product_id,
        'name': product_name,
        'price': product_price,
        'url': product_url,
        'brand': product_brand,
        'feedbackPoints': feedback_points,
        'supplier': supplier,
        'supplierRating': supplier_rating,
        'entity': entity
    }

    # Используем pd.concat для добавления новой строки
    df = pd.concat([df, pd.DataFrame([new_row])])

    # Сохраняем DataFrame обратно в CSV файл без пустых строк
    df.dropna(how='all', inplace=True)  # Удаляем пустые строки, если они есть
    df.to_csv(f'{filename}.csv', index=False, sep=',')


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
    await create_csv(search_item)  # Создаем CSV файл один раз в начале
    total_results = await fetch_total_results(search_item)
    total_pages = (total_results // 100) + 2

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

                    feedback_points = product.get('feedbackPoints', 0)
                    product_brand = product.get('brand', 'Неизвестно')
                    supplier = product.get('supplier', 'Неизвестно')
                    supplier_rating = product.get('supplierRating', 0)
                    entity = product.get('entity', 'Неизвестно')

                    await save_to_csv(product_id, name, price, create_url, product_brand, feedback_points, supplier, supplier_rating, entity, search_item)

                except Exception as e:
                    print(f"Ошибка в обработке продукта {product_id}: {e}")

        else:
            print(f"Ошибка при запросе страницы {page}: {response.status_code}")
