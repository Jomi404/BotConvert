import aiogram.exceptions
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram import F
from aiogram import types
from aiogram.fsm.context import FSMContext
import re
from aiogram.utils.markdown import hlink

from filters import IsAdmin
from utils import bot
from utils import dp
from utils import db
from keyboards import getAdminKeyboard
from keyboards import getKeyboardConfirm
from states import EditMessage

chatNames = ''


@dp.message(IsAdmin(), Command('admin'))
async def admCmd(message: Message):
    keyboard = await getAdminKeyboard()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Админ панель\n'
                                'Выберите действие:', reply_markup=keyboard)


@dp.message(~IsAdmin(), Command('admin'))
async def noAdmCmd(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text='Вы не являетесь Администратором канала. Данный '
                                                              'функционал вам не доступен')


@dp.callback_query(F.data.startswith("change_url"))
async def changeUrl(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text='Отправьте ссылку на канал')
    await state.set_state(EditMessage.waitingUrl)


@dp.message(StateFilter(EditMessage.waitingUrl), F.text)
async def getUrlEdit(message: Message, state: FSMContext):
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                       message.text)
    if links:
        name_chat = message.text.split('/')[-1]
        global chatNames
        chatNames = name_chat
        dataChannel = await bot.get_chat(chat_id=f'@{name_chat}')
        link = dataChannel.invite_link
        titleChannel = dataChannel.title
        hyperlink = hlink(titleChannel, link)
        keyboard = await getKeyboardConfirm()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Теперь ваш текст выглядит так:\nСперва подпишись на канал {hyperlink}',
                               parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard)
    else:
        await message.reply("Вы отправили текст, не содержащий ссылок.")


@dp.callback_query(F.data.startswith("save_change"))
async def saveChange(callback: types.CallbackQuery, state: FSMContext):
    print(chatNames)
    dataChannel = await bot.get_chat(chat_id=f'@{chatNames}')
    db.updateDataChannel(nameChannel=chatNames, newDataChannel=dataChannel)
    await callback.answer(text='Ссылка успешно изменена')
    await state.set_state(None)
