from aiogram.dispatcher.fsm.state import State

from bot.bot import DPBot
from bot.routers.common.keyboards import KEYBOARD_ON_HOLD, KEYBOARD_YES_NO
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from services.player_service import PlayerDataService
from bot.states import RootState
from bot.data_types import IncomingMessage


class WellcomeHandler(Handler):
    def __init__(self, bot: DPBot, player_data_service: PlayerDataService) -> None:
        super().__init__(bot)
        self._player_data_service: PlayerDataService = player_data_service

    async def handle_enter(self, message: IncomingMessage, _: ContextService) -> State:
        identificator = message.user_id
        name = message.chat.first_name
        reply_message = (
            f'Nice to meet you, {name}! I am a bot that helps you manage the Poker on Bones game! '
        )

        player = await self._player_data_service.get_player_by_identificator(identificator)
        if not player:
            reply_message += (
                ' I have not found you in my annals of history. Can I register you as a new player?'
            )
            reply_markup = KEYBOARD_YES_NO
            state = RootState.TG_PLAYER_REGISTRATION
        else:
            reply_markup = KEYBOARD_ON_HOLD
            state = RootState.ON_HOLD
        await self.bot.send(
            chat_id=message.chat.id,
            text=reply_message,
            reply_markup=reply_markup
        )
        return state
