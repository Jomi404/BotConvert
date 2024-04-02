from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message
from utils import getUserChannelStatus


class IsSubscrib(Filter):

    async def __call__(self, message: Message) -> bool:
        user_channel_status = await getUserChannelStatus(message.from_user.id)
        return False if isinstance(user_channel_status, types.ChatMemberLeft) else True
