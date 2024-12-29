import re

import validators

def vol_video_host(e):
    if 0 <= e <= 11:
        t = "01"
    elif e <= 23:
        t = "02"
    elif e <= 35:
        t = "03"
    elif e <= 47:
        t = "04"
    elif e <= 59:
        t = "05"
    elif e <= 71:
        t = "06"
    elif e <= 83:
        t = "07"
    elif e <= 95:
        t = "08"
    elif e <= 107:
        t = "09"
    elif e <= 119:
        t = "10"
    elif e <= 131:
        t = "11"
    elif e <= 143:
        t = "12"
    else:
        t = "13"

    return f"videonme-basket-{t}.wbbasket.ru"


def construct_host_v2(e, t="nm"):
    try:
        n = int(__get_item_id2(e))
    except ValueError:
        return None  # Возвращаем None, если не удалось преобразовать в int

    r = n % 144 if t == "video" else n // 100000
    o = n // 10000 if t == "video" else n // 1000

    if t == "video":
        s = vol_video_host(r)
        video_url = f"https://{s}/vol{r}/part{o}/{n}/mp4/360p/1.mp4"
        return video_url
    else:
        return None  # Возвращаем None для других типов


# Пример использования
def __get_item_id2(url):
    if validators.url(url):
        regex = "(?<=catalog/).+(?=/detail)"
        match = re.search(regex, url)
        if match:
            return match[0]
    else:
        return url

    raise ValueError("Не удалось извлечь item_id из URL")
