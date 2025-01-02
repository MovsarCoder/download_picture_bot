import requests
import pandas as pd


def create_excel():
    # Создаем DataFrame с заголовками
    df = pd.DataFrame(columns=['id', 'name', 'price', 'url', 'brand', 'feedbackPoints', 'supplier', 'supplierRating', 'entity'])
    df.to_excel('wb_data.xlsx', index=False)


def save_to_excel(product_id, product_name, product_price, product_url, product_brand, feedback_points, supplier, supplier_rating, entity):
    # Загружаем существующий файл или создаем новый DataFrame
    try:
        df = pd.read_excel('wb_data.xlsx')
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
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Сохраняем DataFrame обратно в Excel файл без пустых строк
    df.dropna(how='all', inplace=True)  # Удаляем пустые строки, если они есть
    df.to_excel('wb_data.xlsx', index=False)


def create_params(page: int, search_item: str):
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


def fetch_total_results(search_item):
    initial_params = create_params(1, search_item)
    response = requests.get('https://search.wb.ru/exactmatch/ru/common/v9/search', params=initial_params)

    if response.status_code == 200:
        return response.json()['data']['total']
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return 0


def main(search_item):
    create_excel()  # Создаем Excel файл один раз в начале
    total_results = fetch_total_results(search_item)
    total_pages = (total_results // 100) + 2

    for page in range(1, total_pages):
        print(f'Страница: {page}')

        params = create_params(page, search_item)
        response = requests.get('https://search.wb.ru/exactmatch/ru/common/v9/search', params=params)

        if response.status_code == 200:
            products = response.json()['data']['products']

            for product in products:  # Проходим по всем продуктам без пропусков
                name = product["name"]
                product_id = product['id']
                create_url = f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx'
                price = product['sizes'][0]['price']['product']
                feedback_points = product['feedbackPoints']
                product_brand = product['brand']
                supplier = product['supplier']
                supplier_rating = product['supplierRating']
                entity = product['entity']

                save_to_excel(product_id, name, price, create_url, product_brand, feedback_points, supplier, supplier_rating, entity)

            print('Все успешно обработано! Файл собран')

        else:
            print(f"Ошибка при запросе страницы {page}: {response.status_code}")


# #
# search_product = input('Введите имя товара который вы ищете: ')
# main(search_product)
