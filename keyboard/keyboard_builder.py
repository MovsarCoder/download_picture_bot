from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_row_keyboards(items: List[str]) -> ReplyKeyboardMarkup:
    """

    :param items:
    :return:
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
