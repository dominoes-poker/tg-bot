from typing import Optional

from aiogram.dispatcher.fsm.state import State

from bot.routers.common.keyboards import KEYBOARD_YES_NO
from bot.routers.player_register.handler import PlayerRegisterHandler
from bot.services.context_service import ContextService
from bot.states import TelegramPlayerRegisterState
from bot.data_types import IncomingMessage


class TelegramPlayerRegisterHandler(PlayerRegisterHandler):
    async def new_player(self, message: IncomingMessage, context_service: ContextService) -> None:
        username = message.chat.username
        if not username:
            await self.ask_username(message, context_service)
            return TelegramPlayerRegisterState.WAIT_USERNAME

        await self.bot.send(
            chat_id = message.user_id,
            text=f'Do you want to be registered as `{username}`?',
            reply_markup=KEYBOARD_YES_NO
        )
        return TelegramPlayerRegisterState.WHAT_USERNAME_USE

    async def use_tg_username(self, message: IncomingMessage,
                              _: ContextService) -> State:
        username = message.chat.username
        identificator = str(message.user_id)
        return await self._register_player(message.user_id, identificator, username)

    async def ask_new_username(self, message: IncomingMessage,
                               context_service: ContextService) -> State:
        await self.ask_username(message, context_service)
        return TelegramPlayerRegisterState.WAIT_USERNAME

    async def use_new_username(self, message: IncomingMessage,
                               _: ContextService) -> Optional[State]:
        username = message.text
        identificator = str(message.user_id)
        if not self._allow_username_pattern.match(username):
            return await self._bad_username_response(message.user_id)

        return await self._register_player(message.user_id, identificator, username)

    @staticmethod
    def _get_final_message(username: str) -> str:
        return f'Congratulations - you have been registered as `{username}`! ' \
                'What do you want next?'
