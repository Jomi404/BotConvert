from utils import db
from utils import bot


async def getUserChannelStatus(user_id):
    dataChannel = db.getDataChannels()
    name_chat = dataChannel.get('username')
    return await bot.get_chat_member(chat_id=f'@{name_chat}', user_id=user_id)