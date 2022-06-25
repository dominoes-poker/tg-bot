from aiogram.dispatcher.fsm.state import State

from bot.bot import TGBot
from bot.routers.common.keyboards import ON_HOLD_KEYBOARD, YES_NO_KEYBOARD
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.player_service import PlayerDataService
from bot.states import RootState
from bot.types import IncommingMessage


class WellcomeHandler(Handler):
    def __init__(self, bot: TGBot, player_data_service: PlayerDataService) -> None:
        super().__init__(bot)
        self._player_data_service: PlayerDataService = player_data_service

    async def handle_enter(self, message: IncommingMessage, _: ContextService) -> State:
        identificator = message.user_id
        name =message.chat.first_name
        reply_message = (
            f'Nice to meet you, {name}! I am a bot that helps you manage the Poker on Bones game! '
        )

        player = await self._player_data_service.get_player_by_identificator(identificator)
        if not player:
            reply_message += (
                ' I have not found you in my annals of history. Can I register you as a new player?'
            )
            reply_markup = YES_NO_KEYBOARD
            state = RootState.TG_PLAYER_REGISTRATION
        else:
            reply_markup = ON_HOLD_KEYBOARD
            state = RootState.ON_HOLD
        await self.bot.send(
            chat_id=message.chat.id,
            text=reply_message,
            reply_markup=reply_markup
        )
        return state
