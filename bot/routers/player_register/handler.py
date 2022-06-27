import re

from aiogram.dispatcher.fsm.state import State

from bot.bot import DPBot
from bot.routers.common.keyboards import KEYBOARD_ON_HOLD
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.player_service import PlayerDataService
from bot.states import RootState
from bot.types import IncommingMessage, Player


class PlayerRegisterHandler(Handler):
    def __init__(self, bot: DPBot, player_data_service: PlayerDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._allow_username_pattern = re.compile(
            r'^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
        )

    async def _register_player(self, chat_id: int, identificator: int,
                               username: str, _: ContextService) -> State:
        player_data = Player(identificator=identificator, username=username)
        await self._player_data_service.register(player_data)

        await self.bot.send(
            chat_id = chat_id,
            text=self._get_final_message(username),
            reply_markup = KEYBOARD_ON_HOLD
        )
        return RootState.ON_HOLD

    async def decline_registration(self, message: IncommingMessage, _: ContextService) -> State:
        await self.bot.send(
            chat_id = message.user_id,
            text='What do you want to do?',
            reply_markup=KEYBOARD_ON_HOLD
        )
        return RootState.ON_HOLD

    @staticmethod
    def _get_final_message(username: str) -> str:
        raise NotImplementedError()

    def _is_valid_username(self, username: str) -> bool:
        return bool(self._allow_username_pattern.match(username))

    async def ask_username(self, message: IncommingMessage, _: ContextService) -> None:
        await self.bot.send(
            chat_id = message.user_id,
            text='Send me username',
        )

    async def _bad_username_response(self, chat_id) -> None:
        message = 'This is a bad name: the username must be 4-20 symbols ' \
                  'and contains letters or numbers. ' \
                  'Please try again'
        await self.bot.send(
                chat_id = chat_id,
                text=message
            )
