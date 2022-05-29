from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from bot.handlers.common.keyboards import ON_HOLD_KEYBOARD, YES_NO_KEYBOARD

from bot.handlers.handler import Handler
from bot.services import GamerDataService
from bot.states import RootState


class WellcomeHandler(Handler):
    def __init__(self, gamer_data_service: GamerDataService) -> None:
        super().__init__()
        self._gamer_data_service = gamer_data_service

    async def handle(self, message: Message, state: FSMContext) -> None:
        username = message.chat.username
        identificator = message.chat.id
        gamer = await self._gamer_data_service.get_gamer(identificator)

        reply_message = f'Nice to meet you, {username}! I am a bot helps you manage the Poker on Bones game! '
        
        if not gamer:
            reply_message += ' I have not found you in my annals of history. Can I register you as a new player?'
            reply_markup = YES_NO_KEYBOARD
            await state.set_state(RootState.GAMER_REGISTER)
        else:
            reply_markup = ON_HOLD_KEYBOARD
            await state.set_state(RootState.ON_HOLD)

        await message.answer(
            text = reply_message,
            reply_markup = reply_markup
        )