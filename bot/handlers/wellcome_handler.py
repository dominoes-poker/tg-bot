from aiogram.dispatcher.fsm.context import FSMContext
from bot.bot import TGBot
from bot.handlers.common.keyboards import ON_HOLD_KEYBOARD, YES_NO_KEYBOARD

from bot.handlers.handler import Handler
from bot.services import GamerDataService
from bot.states import RootState
from bot.types import IncommingMessage


class WellcomeHandler(Handler):
    def __init__(self, bot: TGBot, gamer_data_service: GamerDataService) -> None:
        super().__init__(bot)
        self._gamer_data_service: GamerDataService = gamer_data_service

    async def enter_handle(self, message: IncommingMessage, state: FSMContext) -> None:
        name = message.chat.first_name
        identificator = message.chat.id

        gamer = await self._gamer_data_service.get_gamer(identificator)
        name = gamer.name if gamer else name

        reply_message = f'Nice to meet you, {name}! I am a bot helps you manage the Poker on Bones game! '

        if not gamer:
            reply_message += ' I have not found you in my annals of history. Can I register you as a new player?'
            reply_markup = YES_NO_KEYBOARD
            await state.set_state(RootState.GAMER_REGISTER)
        else:
            reply_markup = ON_HOLD_KEYBOARD
            await state.set_state(RootState.ON_HOLD)

        return await self._bot.send(
            chat_id=message.chat.id,
            text=reply_message,
            reply_markup=reply_markup
        )
