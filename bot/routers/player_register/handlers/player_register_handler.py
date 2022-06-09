import re
from bot.bot import TGBot

from bot.routers.handlers.common.keyboards import ON_HOLD_KEYBOARD
from bot.routers.handlers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.player_service import PlayerDataService
from bot.states import RootState
from bot.types import IncommingMessage, Player


class PlayerRegisterHandler(Handler):
    def __init__(self, bot: TGBot, player_data_service: PlayerDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._allow_username_pattern = re.compile(r'^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$')
    
    @staticmethod
    def _get_final_message(username: str) -> str:
        raise NotImplementedError

    @classmethod
    def _is_valid_username(cls, username: str) -> bool:
        if cls._allow_username_pattern.match(username):
            return True
        return False

    async def ask_username(self, message: IncommingMessage, context_service: ContextService) -> None:
        return await self.bot.send(
            chat_id = message.user_id,
            text='Send me username',
        )

    async def _register_player(self, chat_id: int, identificator: int, username: str, context_service: ContextService) -> None:
        player_data = Player(identificator=identificator, username=username)
        await self._player_data_service.register(player_data)

        await self.bot.send(
            chat_id = chat_id,
            text=self._get_final_message(username),
            reply_markup = ON_HOLD_KEYBOARD
        )
        await context_service.set_state(RootState.ON_HOLD)
        
    async def _bad_username_response(self, chat_id) -> None:
        return await self.bot.send(
                chat_id = chat_id,
                text='This is a bad name: the username must be 4-20 symbols and contains letters or numbers. Please try again',
            )
            
    async def decline_registration(self, message: IncommingMessage, context_service: ContextService) -> None:
        await self.bot.send(
            chat_id = message.user_id,
            text='What do you want to do?',
            reply_markup=ON_HOLD_KEYBOARD
        )
        await context_service.set_state(RootState.ON_HOLD)