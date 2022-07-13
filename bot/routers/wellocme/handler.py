from aiogram.dispatcher.fsm.state import State

from bot.bot import DPBot
from bot.messages.service import MessageService
from bot.routers.common.keyboards import KEYBOARD_ON_HOLD, KEYBOARD_YES_NO
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from services.player_service import PlayerDataService
from bot.states import RootState
from bot.data_types import IncomingMessage


class WellcomeHandler(Handler):
    def __init__(self, bot: DPBot, message_service: MessageService, player_data_service: PlayerDataService) -> None:
        super().__init__(bot, message_service)
        self._player_data_service: PlayerDataService = player_data_service

    async def handle_enter(self, message: IncomingMessage, _: ContextService) -> State:
        identificator = message.user_id
        name = message.chat.first_name

        reply_message = self._message_service.get_formatted_message('wellcome', name=name)

        player = await self._player_data_service.get_player_by_identificator(identificator)
        if not player:
            reply_message += f' {self._message_service.no_registered_user}'
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
