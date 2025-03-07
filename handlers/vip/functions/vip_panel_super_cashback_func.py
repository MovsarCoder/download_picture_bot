import asyncio
import aiohttp
import aiofiles
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, как Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru,en;q=0.9",
    "Referer": "https://www.wildberries.ru/",
}

BASE_URL = "https://search.wb.ru/exactmatch/ru/common/v9/search"


async def create_csv(filename):
    """Создаёт CSV-файл с заголовками, если его нет."""
    async with aiofiles.open(f"{filename}.csv", mode="w", encoding="utf-8", newline="") as f:
        await f.write("id,name,brand,feedbacks,price,feedbackPoints,url,rating,supplier,supplierRating,entity\n")


async def save_to_csv(products, filename):
    """Записывает список товаров в CSV-файл за один раз."""
    async with aiofiles.open(f"{filename}.csv", mode="a", encoding="utf-8", newline="") as f:
        for product in products:
            row = ",".join(map(str, [
                product["id"], product["name"], product["brand"], product["feedbacks"],
                product["price"], product["feedbackPoints"], product["url"],
                product["rating"], product["supplier"], product["supplierRating"], product["entity"]
            ])) + "\n"
            await f.write(row)


async def fetch_total_results(search_item):
    """Определяет общее количество товаров и рассчитывает число страниц."""
    params = {
        "ab_testid": "boost_promo_5",
        "appType": "1",
        "curr": "rub",
        "dest": "-1257786",
        "ffeedbackpoints": "1",
        "hide_dtype": "10",
        "lang": "ru",
        "page": "1",
        "query": search_item,
        "resultset": "catalog",
        "sort": "popular",
        "spp": "30",
        "suppressSpellcheck": "false",
    }

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        try:
            async with session.get(BASE_URL, params=params, headers=HEADERS, timeout=10) as response:
                if response.status == 200:
                    text = await response.text()
                    try:
                        data = json.loads(text)  # Принудительно парсим JSON из текста
                        total_results = data.get("data", {}).get("total", 0)
                        return (total_results // 100) + 2
                    except json.JSONDecodeError:
                        print("[Ошибка] Сервер вернул некорректный JSON. Пропускаем.")
                        return 0
                else:
                    print(f"[Ошибка] Не удалось получить количество товаров: {response.status}")
                    return 0
        except Exception as e:
            print(f"[Ошибка] Ошибка при получении общего количества товаров: {e}")
            return 0


async def fetch_page(session, page, search_item):
    """Запрашивает страницу товаров и парсит JSON."""
    params = {
        "ab_testid": "boost_promo_5",
        "appType": "1",
        "curr": "rub",
        "dest": "-1257786",
        "ffeedbackpoints": "1",
        "hide_dtype": "10",
        "lang": "ru",
        "page": str(page),
        "query": search_item,
        "resultset": "catalog",
        "sort": "popular",
        "spp": "30",
        "suppressSpellcheck": "false",
    }

    try:
        async with session.get(BASE_URL, params=params, headers=HEADERS, timeout=10) as response:
            if response.status != 200:
                print(f"[Ошибка] Код ответа {response.status} на странице {page}. Пропускаем.")
                return []

            text = await response.text()
            try:
                data = json.loads(text)
                products = data.get("data", {}).get("products", [])
            except json.JSONDecodeError:
                print(f"[Ошибка] Сервер вернул некорректный JSON на странице {page}. Пропускаем.")
                return []

            parsed_products = []
            for product in products:
                product_id = product.get("id", 0)
                name = product.get("name", "Неизвестно")
                create_url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"

                # Проверяем наличие цены
                if "sizes" in product and product["sizes"]:
                    price = product["sizes"][0].get("price", {}).get("product", 0) // 100
                    if price == 0:
                        print(f"У продукта {product_id} отсутствует цена. Пропускаем.")
                        continue
                else:
                    print(f"У продукта {product_id} отсутствует массив 'sizes'. Пропускаем.")
                    continue

                feedback_points = product.get("feedbackPoints", 0)

                # Фильтр по feedbackPoints
                if feedback_points >= price // 2 and feedback_points > (price * 0.25) / 2:
                    parsed_products.append({
                        "id": product_id,
                        "name": name,
                        "brand": product.get("brand", "Неизвестно"),
                        "feedbacks": product.get("feedbacks", 0),
                        "price": price,
                        "feedbackPoints": feedback_points,
                        "url": create_url,
                        "rating": product.get("reviewRating", 0),
                        "supplier": product.get("supplier", "Неизвестно"),
                        "supplierRating": product.get("supplierRating", 0),
                        "entity": product.get("entity", "Неизвестно"),
                    })

            return parsed_products

    except Exception as e:
        print(f"[Ошибка] Не удалось обработать страницу {page}: {e}")
        return []


async def main(search_item):
    """Основная функция парсинга Wildberries."""
    await create_csv(search_item)  # Создаём CSV файл

    total_pages = await fetch_total_results(search_item)
    if total_pages == 0:
        print("[Ошибка] Не удалось определить количество страниц.")
        return

    # print(f"Будет спарсено {total_pages} страниц...")

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        tasks = [fetch_page(session, page, search_item) for page in range(1, total_pages + 1)]
        all_results = await asyncio.gather(*tasks)

    # Собираем все товары в один список
    all_products = [p for products in all_results for p in products if products]

    if all_products:
        # Сортируем товары по цене перед записью
        all_products.sort(key=lambda x: x["price"])
        await save_to_csv(all_products, search_item)  # Сохраняем все товары за один раз


