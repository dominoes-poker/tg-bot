from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot.bot import TGBot
from bot.handlers.common.keyboards import ON_HOLD_KEYBOARD
from bot.handlers.handler import Handler
from bot.services import GamerDataService
from bot.states import GamerRegisterState, RootState
from bot.types import Gamer, IncommingMessage


class GamerRegisterHandler(Handler):
    def __init__(self, bot: TGBot, gamer_data_service: GamerDataService) -> None:
        super().__init__(bot)
        self._gamer_data_service = gamer_data_service

    async def ask_name(self, message: IncommingMessage, state: FSMContext) -> None:
        await self._bot.send(
            chat_id = message.chat.id,
            text='Great! Send me your name',
            reply_markup=ReplyKeyboardRemove
        )
        await state.set_state(GamerRegisterState.NAME)

    async def handle_name(self, message: IncommingMessage, state: FSMContext) -> None:
        await state.update_data({'name': message.text})
        await self._bot.send(
            chat_id = message.chat.id,
            text=f'Ok, I will call you {message.text}. Now send me your username.',
            reply_markup = ReplyKeyboardRemove
        )
        await state.set_state(GamerRegisterState.USERNAME)

    async def handle_username(self, message: IncommingMessage, state: FSMContext) -> None:
        await state.update_data({'username': message.text})
        data = await state.get_data()
        gamer = Gamer(name=data['name'], username=['username'], identificator=message.user_id)
        gamer = await self._gamer_data_service.register(gamer)
        await self._bot.send(
            chat_id = message.chat.id,
            text='Ok, I got it. What do you want next?',
            reply_markup = ON_HOLD_KEYBOARD
        )
        await state.set_state(RootState.ON_HOLD)
