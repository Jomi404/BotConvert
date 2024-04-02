from aiogram.utils.markdown import hlink

from utils import db
from utils import bot


async def getHyperLink():
    dataChannel = db.getDataChannels()
    name_chat = dataChannel.get('username')
    titleChannel = dataChannel.get('title')
    link = await bot.export_chat_invite_link(chat_id=f'@{name_chat}')
    hyperlink = hlink(titleChannel, link)
    return hyperlink
