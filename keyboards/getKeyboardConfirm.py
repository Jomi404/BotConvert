from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


async def getKeyboardConfirm():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Сохранить изменения', callback_data='save_change'))
    keyboard.add(types.InlineKeyboardButton(text='Отменить изменения', callback_data='del_change'))
    keyboard.adjust(2)
    return keyboard.as_markup()
