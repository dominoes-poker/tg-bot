from typing import Iterable, List, Set
from bot.bot import TGBot

from bot.routers.handlers.common.keyboards import YES_NO_KEYBOARD, keyboard_from_data, keyboard_round
from bot.routers.handlers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import GameState
from bot.types import IncommingMessage


class CreateGameHandler(Handler):
    def __init__(self, bot: TGBot, 
                 player_data_service: PlayerDataService,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._game_data_service = game_data_service

    async def ask_player_usernames(self, message: IncommingMessage, context_service: ContextService) -> None:
        await self.bot.send(
            chat_id=message.user_id,
            text='Ok, lets start a new game. Who will play with you? Send me usernames of every player',
        )
        await context_service.set_state(GameState.WAIT_PLAYER_USERNAMES)

    async def handle_player_usernames(self, message: IncommingMessage, context_service: ContextService) -> None:
        player_usernames = self._process_names(message.text.split(','))
        players = await self._player_data_service.get_players_by_username(player_usernames)
        if len(players) != len(player_usernames):
            ...
        game = await self._game_data_service.create(players=players)
        await context_service.set_current_game_id(game)
        await self.bot.send(
            chat_id=message.user_id,
            text='Great! We are ready to start the first round',
            reply_markup=keyboard_round(1)
        )
        await context_service.set_state(GameState.START_ROUND)
        

    @staticmethod
    def _process_names(names: Iterable[str]) -> Set[str]:
        result = set()
        for name in names:
            name = name.strip()
            result.add(name)
        return result
