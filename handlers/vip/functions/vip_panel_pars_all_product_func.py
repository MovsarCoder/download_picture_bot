import asyncio
import aiohttp
import aiofiles
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru,en;q=0.9",
    "Referer": "https://www.wildberries.ru/",
}


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

async def fetch_page(session, page, search_item):
    """Запрашивает страницу товаров и парсит JSON."""
    url = "https://search.wb.ru/exactmatch/ru/common/v9/search"
    params = {
        "ab_testid": "boost_promo_5",
        "appType": "1",
        "curr": "rub",
        "dest": "-1257786",
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
        async with session.get(url, params=params, headers=HEADERS) as response:
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                data = await response.json()
            else:
                text = await response.text()
                try:
                    data = json.loads(text)  # Пробуем вручную конвертировать в JSON
                except json.JSONDecodeError:
                    print(f"[Ошибка] Сервер вернул некорректный JSON на странице {page}. Пропускаем.")
                    return []

            products = data.get("data", {}).get("products", [])

            parsed_products = []
            for product in products:
                product_id = product.get("id", 0)
                name = product.get("name", "Неизвестно")
                create_url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"

                price = next((size["price"]["product"] // 100 for size in product.get("sizes", []) if "price" in size), 0)

                parsed_products.append({
                    "id": product_id,
                    "name": name,
                    "brand": product.get("brand", "Неизвестно"),
                    "feedbacks": product.get("feedbacks", 0),
                    "price": price,
                    "feedbackPoints": product.get("feedbackPoints", 0),
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

    total_pages = 20  # Ограничиваем 20 страниц для скорости

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, page, search_item) for page in range(1, total_pages)]
        all_results = await asyncio.gather(*tasks)

    # Собираем все товары в один список
    all_products = [product for products in all_results for product in products]

    if all_products:
        await save_to_csv(all_products, search_item)  # Сохраняем все товары за один раз

