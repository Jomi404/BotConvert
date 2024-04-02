from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


async def getKeyboardCheck():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text='Проверить✅', callback_data='check'))
    return keyboard.as_markup()
