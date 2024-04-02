from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message
from utils import db


class IsAdmin(Filter):

    async def __call__(self, message: Message) -> bool:
        AdminList = db.getAdminList()
        return str(message.from_user.id) in AdminList
