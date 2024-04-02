from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


async def getAdminKeyboard():
    """return keyboard.as_markup()"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text='Редактировать ссылку✏️', callback_data='change_url'))
    #keyboard.row(types.InlineKeyboardButton(text='Получить список подписчиков', callback_data='get_subscribers'))
    return keyboard.as_markup()
