from aiogram.fsm.state import StatesGroup, State


class EditMessage(StatesGroup):
    waitingUrl = State()
    isLink = State()
    noLink = State()

