from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from bot.handlers.common.keyboards import ON_HOLD_KEYBOARD, YES_NO_KEYBOARD

from bot.handlers.handler import Handler
from bot.services import GamerDataService
from bot.states import GamerRegisterState


class GamerRegisterHandler(Handler):
    def __init__(self, gamer_data_service: GamerDataService) -> None:
        super().__init__()
        self._gamer_data_service = gamer_data_service

    async def ask_name(self, message: Message, state: FSMContext) -> None:
        await message.answer(
            text='Great! Send me your name',
            reply_markup = ReplyKeyboardRemove
        )
        await state.set_state(GamerRegisterState.NAME)

    async def handle_name(self, message: Message, state: FSMContext) -> None:
        await state.set_data({'name': message.text})
        await message.answer(
            text=f'Ok, will call you {message.text}. Now send me your username',
            reply_markup = ReplyKeyboardRemove
        )
        await state.set_state(GamerRegisterState.USERNAME)

    async def handle_username(self, message: Message, state: FSMContext) -> None:
        await state.set_data({'username': message.text})
        await message.answer(
            text=f'Ok, I got it',
            reply_markup = ReplyKeyboardRemove
        )
        await state.set_state(GamerRegisterState.USERNAME)