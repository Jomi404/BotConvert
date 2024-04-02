import aiogram.exceptions
from aiogram.filters import CommandStart, StateFilter
import aiogram.exceptions
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram import types
from pyrogram import enums
from aiogram.fsm.context import FSMContext
import re
from aiogram.utils.markdown import hlink

from utils import db
from keyboards import getAdminKeyboard
from keyboards import getKeyboardConfirm
from states import EditMessage

from filters import IsSubscrib
from filters import IsAdmin
from keyboards import getKeyboardCheck
from utils import bot
from utils import dp
from utils import getHyperLink

temp = []


@dp.message(IsSubscrib(), CommandStart())
async def subCmdStart(message: Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Это бот позволяет легко конвертировать документы из одного формата в другой.'
                                'Просто отправьте нужный документ!')


@dp.message(~IsSubscrib(), CommandStart())
async def subCmdStart(message: Message):
    hyperlink = await getHyperLink()
    keyboard = await getKeyboardCheck()
    msg = await bot.send_message(chat_id=message.from_user.id, text=f'Сперва подпишись на канал {hyperlink}',
                                 parse_mode="HTML", reply_markup=keyboard, disable_web_page_preview=True)

    temp.append(msg.message_id)
    temp.append(message.message_id)


@dp.message(~IsSubscrib())
async def NotSubscriber(message: Message):
    hyperlink = await getHyperLink()
    keyboard = await getKeyboardCheck()

    msg = await bot.send_message(chat_id=message.from_user.id, text=f'Сперва подпишись на канал {hyperlink}',
                                 parse_mode="HTML", reply_markup=keyboard, disable_web_page_preview=True)
    temp.append(msg.message_id)
    temp.append(message.message_id)


@dp.callback_query(~IsSubscrib(), F.data.startswith("check"))
async def checkSubscribe(callback: types.CallbackQuery):
    await callback.answer(cache_time=1)
    keyboard = await getKeyboardCheck()
    hyperlink = await getHyperLink()
    msg = await bot.send_message(chat_id=callback.from_user.id, text=f'Сперва подпишись на канал {hyperlink}',
                                 parse_mode="HTML", reply_markup=keyboard, disable_web_page_preview=True)
    temp.append(msg.message_id)


@dp.callback_query(IsSubscrib(), F.data.startswith("check"))
async def checkSubscribe(callback: types.CallbackQuery):
    for n_message in temp:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=n_message)
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Это бот позволяет легко конвертировать документы из одного формата в другой.'
                                'Просто отправьте нужный документ!', reply_markup=None)


# добавить проверку на размер
@dp.message(IsSubscrib(), F.document)
async def sendDocument(message: Message):
    global file_obj
    file_type = ''
    err = False
    document = message.document
    filename = document.file_name
    file_id = document.file_id
    try:
        file_obj = await bot.get_file(file_id)
        file_type = file_obj.file_path.split('.')[-1]
    except aiogram.exceptions.TelegramBadRequest:
        err = True
    finally:
        if err:
            await message.reply(text='Вы не можете отправлять файлы размером более 20 МБ из-за ограничения Telegram '
                                     'API.')
        else:
            # скачивание файла
            await bot.download(file=file_id, destination=f'./data/save_files/{file_id}.{file_type}')
            await message.reply(text=f'Тип файла - {file_type} (💼 Документ)\nНазвание вашего файла: {filename}')


@dp.message(IsSubscrib(), F.photo)
async def sendPhoto(message: Message):
    image_url = ''
    photo_type = ''
    photo = message.photo[-1]
    err = False
    try:
        photo_obj = await bot.get_file(photo.file_id)
        photo_type = photo_obj.file_path.split('.')[-1]
        image_url = f"./data/save_files/{message.photo[-1].file_id}.{photo_type}"
    except aiogram.exceptions.TelegramBadRequest:
        err = True
    finally:
        if err:
            await message.reply(text='Вы не можете отправлять файлы размером более 20 МБ из-за ограничения Telegram '
                                     'API.')
        else:
            # скачивание файла
            await bot.download(photo, destination=image_url)
            await message.reply(text=f'Тип файла - {photo_type} (📷 Изображение)')



chatNames = []


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
    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id, text='Отправьте ссылку на канал')
    await state.set_state(EditMessage.waitingUrl)



@dp.message(StateFilter(EditMessage.waitingUrl), F.text)
async def getUrlEdit(message: Message, state: FSMContext):
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                       message.text)
    if links:
        name_chat = message.text.split('/')[-1]
        dataChannel = await bot.get_chat(chat_id=f'@{name_chat}')
        print(dataChannel.model_dump_json())
        chatNames.append(dataChannel.username)
        link = dataChannel.invite_link
        titleChannel = dataChannel.title
        hyperlink = hlink(titleChannel, link)
        keyboard = await getKeyboardConfirm()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Теперь ваш текст выглядит так:\nСперва подпишись на канал {hyperlink}',
                               parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard)
        await state.set_state(EditMessage.isLink)
    else:
        await message.reply("Вы отправили текст, не содержащий ссылок.")


@dp.callback_query(StateFilter(EditMessage.isLink), F.data.startswith("save_change"))
async def saveChange(callback: types.CallbackQuery, state: FSMContext):
    dataChannel = await bot.get_chat(chat_id=f'@{chatNames[-1]}')
    db.query('UPDATE channels set username = ?, title = ? WHERE id = 1', (chatNames[-1], dataChannel.title))
    await callback.answer(text='Ссылка успешно изменена✅', cache_time=1)
    await callback.message.delete()
    await state.set_state(None)


@dp.callback_query(StateFilter(EditMessage.isLink), F.data.startswith("del_change"))
async def saveChange(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(text='Вы отменили обновление ссылки канала❌', cache_time=1)
    await bot.send_message(chat_id=callback.from_user.id, text='Вы отменили обновление ссылки канала. Используйте '
                                                               '/admin, чтобы внести изменения.')
    await callback.message.delete()
    await state.set_state(None)


@dp.callback_query(F.data.startswith("get_subscribers"))
async def getSubscibers(callback: types.CallbackQuery):
    dataChannel = db.getDataChannels()


@dp.message(IsSubscrib(), F.text)
async def existType(message: Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Это бот позволяет легко конвертировать документы💼 или фото📷 из одного формата в '
                                'другой.')
