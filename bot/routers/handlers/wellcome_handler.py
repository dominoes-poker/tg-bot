from bot.bot import TGBot
from bot.context import TGContext
from bot.routers.handlers.common.keyboards import ON_HOLD_KEYBOARD, YES_NO_KEYBOARD

from bot.routers.handlers.handler import Handler
from bot.services.gamer_service import GamerDataService
from bot.states import RootState
from bot.types import IncommingMessage


class WellcomeHandler(Handler):
    def __init__(self, bot: TGBot, gamer_data_service: GamerDataService) -> None:
        super().__init__(bot)
        self._gamer_data_service: GamerDataService = gamer_data_service

    async def handle_enter(self, message: IncommingMessage, context: TGContext) -> None:
        identificator = message.user_id
        gamer = await self._gamer_data_service.get_gamer(identificator)
        name = gamer.name if gamer else message.chat.first_name

        reply_message = f'Nice to meet you, {name}! I am a bot helps you manage the Poker on Bones game! '

        if not gamer:
            reply_message += ' I have not found you in my annals of history. Can I register you as a new player?'
            reply_markup = YES_NO_KEYBOARD
            await context.set_state(RootState.GAMER_REGISTER)
        else:
            reply_markup = ON_HOLD_KEYBOARD
            await context.set_state(RootState.ON_HOLD)
            await context.set_gamer(gamer)
        return await self.bot.send(
            chat_id=message.chat.id,
            text=reply_message,
            reply_markup=reply_markup
        )
