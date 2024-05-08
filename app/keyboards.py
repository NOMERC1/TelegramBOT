from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton)
from app.database.requests import get_distances, get_distance_date
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='Результаты марафонов')],
                                     [KeyboardButton(text='Помощь'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню ...')

async def distances():
    all_distances = await get_distances()
    keyboard = InlineKeyboardBuilder()
    for distance in all_distances:
        keyboard.add(InlineKeyboardButton(text=distance.distance, callback_data=f"distance_{distance.id}"))
    return keyboard.adjust(2).as_markup()

async def dates(distance_id):
    all_dates = await get_distance_date(distance_id)
    keyboard = InlineKeyboardBuilder()
    for date in all_dates:
        keyboard.add(InlineKeyboardButton(text=date.date, callback_data=f"date_{date.id}"))
    return keyboard.adjust(2).as_markup()