import re
from bot.bot import TGBot
from bot.context import TGContext

from bot.routers.handlers.common.keyboards import ON_HOLD_KEYBOARD
from bot.routers.handlers.handler import Handler
from bot.services.gamer_service import GamerDataService
from bot.states import GamerRegisterState, RootState
from bot.types import Gamer, IncommingMessage


class GamerRegisterHandler(Handler):
    def __init__(self, bot: TGBot, gamer_data_service: GamerDataService) -> None:
        super().__init__(bot)
        self._gamer_data_service = gamer_data_service
        self._allow_name_pattern = re.compile(r'^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$')

    async def ask_username(self, message: IncommingMessage, context: TGContext) -> None:
        await self.bot.send(
            chat_id = message.chat.id,
            text='Great! Send me your name',
        )
        await context.set_state(GamerRegisterState.WAIT_USERNAME)

    async def handle_username(self, message: IncommingMessage, context: TGContext) -> None:
        name = message.text
        if not self._allow_name_pattern.match(name):
            return await self.bot.send(
                chat_id = message.chat.id,
                text='This is a bad name, please try again',
            )
        gamer_data = Gamer(name=message.text, identificator=message.user_id)
        registred_gamer = await self._gamer_data_service.register(gamer_data)
        
        await self.bot.send(
            chat_id = message.chat.id,
            text='Ok, I got it. What do you want next?',
            reply_markup = ON_HOLD_KEYBOARD
        )
        
        await context.set_state(RootState.ON_HOLD)
        await context.set_gamer(registred_gamer)
